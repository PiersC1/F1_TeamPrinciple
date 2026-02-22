import pygame
import pygame_gui
from src.views.base_view import BaseView

class RDView(BaseView):
    """View rendering the HoI4-style focus tree and allowing project selection."""

    def on_enter(self):
        super().on_enter()
        self.background = pygame.Surface(self.window_surface.get_size())
        self.background.fill(pygame.Color('#2C3A47')) # Slightly different grey
        
        # --- Top Navigation Bar ---
        self.lbl_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (300, 40)),
            text="Research & Development",
            manager=self.ui_manager
        )
        
        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((650, 10), (120, 40)),
            text='< Back',
            manager=self.ui_manager
        )

        # --- Active Project Panel ---
        self.panel_active = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((20, 80), (750, 80)),
            manager=self.ui_manager
        )
        
        rd = self.game_state.rd_manager
        if rd.active_project:
            status_text = f"Current Project: {rd.active_project.name} ({rd.active_project.progress_time}/{rd.active_project.base_time_to_complete} Races)"
        else:
            status_text = "No Active R&D Project. Assign one below."
            
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 20), (700, 30)),
            text=status_text,
            manager=self.ui_manager,
            container=self.panel_active
        )
        
        # --- List of Available Nodes (Simulating a simple tree for MVP) ---
        # Drawing an entire visual tree in Pygame is extremely complex. 
        # For MVP, we render a scrollable list of AVAILABLE and LOCKED projects 
        # to show the dependencies and tradeoffs clearly.
        
        self.panel_tree = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((20, 180), (750, 380)),
            manager=self.ui_manager
        )
        
        y_offset = 10
        self.action_buttons = {} # map button element to node_id
        
        for node_id, node in rd.nodes.items():
            # Node Card
            bg_color = '#ffffff' # White for locked
            if node.state == "COMPLETED": bg_color = '#78e08f' # Green
            if node.state == "LOCKED": bg_color = '#b2bec3' # Greyed out
            if node.state == "AVAILABLE": bg_color = '#ffeaa7' # Yellow
            if node.state == "MUTUALLY_LOCKED": bg_color = '#ff7675' # Red
            if node.state == "IN_PROGRESS": bg_color = '#74b9ff' # Blue

            card_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((10, y_offset), (700, 110)),
                manager=self.ui_manager,
                container=self.panel_tree
            )
            
            # Title & State
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 5), (300, 20)),
                text=f"{node.name} [{node.state}]",
                manager=self.ui_manager,
                container=card_panel
            )
            
            # Description
            pygame_gui.elements.UITextBox(
                html_text=f"{node.description}",
                relative_rect=pygame.Rect((10, 30), (450, 45)),
                manager=self.ui_manager,
                container=card_panel
            )
            
            # Tradeoffs string
            tradeoff_str = " | ".join([f"{k.split('.')[1]}: {v}" for k,v in node.effects.items()])
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 75), (450, 20)),
                text=f"Effects: {tradeoff_str}",
                manager=self.ui_manager,
                container=card_panel
            )

            # Action Button
            if node.state == "AVAILABLE" and not rd.active_project:
                btn = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((480, 20), (200, 40)),
                    text=f"Start (${node.cost:,})",
                    manager=self.ui_manager,
                    container=card_panel
                )
                self.action_buttons[btn] = node.node_id
            
            y_offset += 120

        # We must call this to update the scrollbar length
        self.panel_tree.set_scrollable_area_dimensions((700, y_offset))

    def draw(self):
        self.window_surface.blit(self.background, (0, 0))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_back:
                return "DASHBOARD"
            
            # Check if an R&D start button was clicked
            if event.ui_element in self.action_buttons:
                node_id = self.action_buttons[event.ui_element]
                node = self.game_state.rd_manager.nodes.get(node_id)
                # Attempt to spend money
                if self.game_state.finance_manager.spend(node.cost):
                    self.game_state.rd_manager.start_project(node_id)
                    # Hack: reload the view completely to reflect new state
                    self.on_exit()
                    self.on_enter()
                else:
                    print("Could not start project - Check Cost Cap or Budget!")
                
        return None
