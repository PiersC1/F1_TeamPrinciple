import pygame
import pygame_gui
from src.views.base_view import BaseView
from src.utils.save_load_manager import SaveLoadManager

class DashboardView(BaseView):
    """The main hub for team management."""

    def on_enter(self):
        super().on_enter()
        self.background = pygame.Surface(self.window_surface.get_size())
        self.background.fill(pygame.Color('#1E272E')) # Dark slate grey
        
        # --- Top Navigation Bar ---
        self.lbl_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (300, 40)),
            text=f"F1 Team Principal - {self.game_state.team_name}",
            manager=self.ui_manager
        )
        
        self.lbl_budget = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((550, 10), (220, 40)),
            text=f"Budget: ${self.game_state.finance_manager.balance:,}",
            manager=self.ui_manager
        )

        # --- Sidebar Navigation ---
        self.btn_rd = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 80), (150, 40)),
            text='R&D Tree',
            manager=self.ui_manager
        )
        
        # --- Main Content Area (Season Summary) ---
        self.panel_overview = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((190, 80), (580, 200)),
            manager=self.ui_manager
        )
        
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            text=f"Season: {self.game_state.season}",
            manager=self.ui_manager,
            container=self.panel_overview
        )
        
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 40), (200, 30)),
            text=f"Completed Races: {self.game_state.current_race_index}",
            manager=self.ui_manager,
            container=self.panel_overview
        )

        overall_perf = self.game_state.car.get_overall_performance()
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 70), (300, 30)),
            text=f"Est. Car Performance Rating: {overall_perf}/100",
            manager=self.ui_manager,
            container=self.panel_overview
        )
        
        # --- Standings Panels ---
        self.panel_standings = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 290), (760, 150)),
            manager=self.ui_manager
        )
        
        # Determine top 5 drivers
        drivers = self.game_state.championship_manager.get_sorted_driver_standings()
        teams = self.game_state.championship_manager.get_sorted_constructor_standings()
        
        drv_text = "<b>Top 5 Drivers:</b><br>"
        for i, (name, pts) in enumerate(drivers[:5]):
            drv_text += f"{i+1}. {name} - {pts} pts<br>"
            
        con_text = "<b>Constructors:</b><br>"
        for i, (name, pts) in enumerate(teams[:5]):
            con_text += f"{i+1}. {name} - {pts} pts<br>"

        pygame_gui.elements.UITextBox(
            html_text=drv_text,
            relative_rect=pygame.Rect((10, 10), (360, 130)),
            manager=self.ui_manager,
            container=self.panel_standings
        )
        
        pygame_gui.elements.UITextBox(
            html_text=con_text,
            relative_rect=pygame.Rect((380, 10), (360, 130)),
            manager=self.ui_manager,
            container=self.panel_standings
        )

        
        # --- Bottom/Action Area ---
        self.btn_next_race = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((550, 500), (200, 60)),
            text='Advance to Next Race',
            manager=self.ui_manager
        )
        
        # Re-introducing MVP Save/Load/Cheat buttons
        self.btn_cheat = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 450), (150, 40)),
            text='Cheat: +$10m',
            manager=self.ui_manager
        )
        self.btn_save = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 500), (150, 40)),
            text='Save Game',
            manager=self.ui_manager
        )
        self.btn_load = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((180, 500), (150, 40)),
            text='Load Game',
            manager=self.ui_manager
        )

    def draw(self):
        self.window_surface.blit(self.background, (0, 0))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_rd:
                return "RD_VIEW" 
                
            elif event.ui_element == self.btn_next_race:
                # Instead of instantly advancing time, go to the Race Weekend screen
                return "RACE_WEEKEND"
                
            elif event.ui_element == self.btn_cheat:
                self.game_state.finance_manager.cheat_add_funds(10_000_000)
                self.on_exit()
                self.on_enter()
                
            elif event.ui_element == self.btn_save:
                slm = SaveLoadManager()
                slm.save_game("slot1", self.game_state.to_dict())
                print("Game Saved!")
                
            elif event.ui_element == self.btn_load:
                slm = SaveLoadManager()
                data = slm.load_game("slot1")
                if data:
                    self.game_state.load_from_dict(data)
                    self.on_exit()
                    self.on_enter()
                    print("Game Loaded!")
                    
        return None
