import pygame
import pygame_gui
from src.views.base_view import BaseView
from src.simulators.race_simulator import RaceSimulator
from src.database.track_database import TrackDatabase

class RaceWeekendView(BaseView):
    """Handles Qualifying display, Strategy selection, and Race simulation."""

    def on_enter(self):
        super().on_enter()
        self.background = pygame.Surface(self.window_surface.get_size())
        self.background.fill(pygame.Color('#192a56')) # Navy blue
        
        # Determine the current track
        calendar = TrackDatabase.get_calendar()
        if self.game_state.current_race_index >= len(calendar):
            self.track = calendar[-1] # Failsafe if we go over 10 races
        else:
            self.track = calendar[self.game_state.current_race_index]
            
        self.state = "PRE_RACE" # PRE_RACE -> POST_RACE
        self.race_results = None

        self._build_pre_race_ui()

    def _build_pre_race_ui(self):
        self.ui_manager.clear_and_reset()
        
        # --- Top Navigation Bar ---
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (500, 40)),
            text=f"Race Weekend - Round {self.game_state.current_race_index + 1}: {self.track.name} ({self.track.country})",
            manager=self.ui_manager
        )
        
        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((650, 10), (120, 40)),
            text='< Back',
            manager=self.ui_manager
        )
        
        # --- Track Info ---
        pygame_gui.elements.UITextBox(
            html_text=f"<b>Track Info:</b> {self.track.laps} Laps<br><b>Aero demand:</b> {self.track.aero_weight}x | <b>Power demand:</b> {self.track.powertrain_weight}x",
            relative_rect=pygame.Rect((20, 60), (750, 60)),
            manager=self.ui_manager
        )
        
        # --- Strategy Selector (Placeholder for logic injection later) ---
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 130), (200, 30)),
            text="Team Strategy:",
            manager=self.ui_manager
        )
        self.dropdown_strategy = pygame_gui.elements.UIDropDownMenu(
            options_list=["Balanced", "Aggressive (High Wear)", "Conserve (Low Wear)"],
            starting_option="Balanced",
            relative_rect=pygame.Rect((20, 160), (200, 40)),
            manager=self.ui_manager
        )

        # --- Simulate Action ---
        self.btn_simulate = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 150), (300, 60)),
            text='Simulate Race',
            manager=self.ui_manager
        )
        
        # --- Pre-Race Grid Standings (Quali Sim Placeholder) ---
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 230), (300, 30)),
            text="Grid Order (Pre-race pace calculation):",
            manager=self.ui_manager
        )
        
        self.list_results = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((20, 260), (750, 300)),
            item_list=[f"No session run yet."],
            manager=self.ui_manager
        )
        
        # Do a quick 1-lap Quali sim just to sort the grid strings
        entries = self.game_state.get_all_race_entries()
        q_sim = RaceSimulator(entries, self.track)
        for e in entries:
            e.current_lap_time = q_sim._calculate_lap_time(e)
        sorted_entries = sorted(entries, key=lambda e: e.current_lap_time)
        
        grid_strings = [f"P{i+1}: {e.driver.name} ({e.team_name}) - {e.current_lap_time:.3f}s" for i, e in enumerate(sorted_entries)]
        self.list_results.set_item_list(grid_strings)

    def _build_post_race_ui(self):
        self.ui_manager.clear_and_reset()
        
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (500, 40)),
            text=f"Race Results - Round {self.game_state.current_race_index}: {self.track.name}",
            manager=self.ui_manager
        )
        
        # Re-purpose the back button to advance to the next week
        self.btn_continue = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((600, 500), (180, 60)),
            text='Continue to Dashboard >',
            manager=self.ui_manager
        )
        
        # Show results
        self.list_results = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((20, 60), (550, 500)),
            item_list=[],
            manager=self.ui_manager
        )
        
        if self.race_results:
            res_strings = []
            for i, r in enumerate(self.race_results["standings"]):
                pts = self.game_state.championship_manager.POINTS_SYSTEM[i] if i < 10 else 0
                res_strings.append(f"P{i+1}: {r['driver']} ({r['team']}) - Time: {r['total_time']:.1f}s - Pts: +{pts}")
            self.list_results.set_item_list(res_strings)
            
    def draw(self):
        self.window_surface.blit(self.background, (0, 0))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            
            if self.state == "PRE_RACE":
                if event.ui_element == self.btn_back:
                    return "DASHBOARD"
                    
                elif event.ui_element == self.btn_simulate:
                    # Execute Race
                    print(f"Simulating: Strategy={self.dropdown_strategy.selected_option}")
                    
                    entries = self.game_state.get_all_race_entries()
                    simulator = RaceSimulator(entries, self.track)
                    self.race_results = simulator.run_race()
                    
                    # Award Championship Points
                    self.game_state.championship_manager.score_points(self.race_results["standings"])
                    
                    # Advance Calendar Global State
                    self.game_state.current_race_index += 1
                    self.game_state.rd_manager.advance_time(1)
                    
                    # Change UI State to Results
                    self.state = "POST_RACE"
                    self._build_post_race_ui()
                    
            elif self.state == "POST_RACE":
                if event.ui_element == self.btn_continue:
                    return "DASHBOARD"
                    
        return None
