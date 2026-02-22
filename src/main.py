import pygame
import pygame_gui
import sys
import os
from pprint import pprint

# Add the project root to the python path so 'from src...' works when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.game_state import GameState
from src.models.personnel.driver import Driver
from src.utils.save_load_manager import SaveLoadManager
from src.views.view_manager import ViewManager
from src.views.dashboard_view import DashboardView
from src.views.rd_view import RDView
from src.views.race_weekend_view import RaceWeekendView

def create_dummy_data(game_state: GameState):
    """Initializes the game state with some dummy drivers for the MVP."""
    print("Initializing new game with dummy data...")
    d1 = Driver("Player Driver 1", 5_000_000, rating=85, speed=88, consistency=90, tire_management=80)
    d2 = Driver("Player Driver 2", 2_000_000, rating=75, speed=78, consistency=70, tire_management=75)
    game_state.drivers.extend([d1, d2])

def main():
    pygame.init()
    
    # 1. Setup Window
    window_surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("F1 Team Principal")
    ui_manager = pygame_gui.UIManager((800, 600))
    
    # 2. Setup Game Logic
    game_state = GameState()
    create_dummy_data(game_state)
    
    # 3. Setup Views
    view_manager = ViewManager()
    
    dashboard_view = DashboardView(ui_manager, game_state, window_surface)
    rd_view = RDView(ui_manager, game_state, window_surface)
    race_view = RaceWeekendView(ui_manager, game_state, window_surface)
    
    # Register Views
    view_manager.register_view("DASHBOARD", dashboard_view)
    view_manager.register_view("RD_VIEW", rd_view)
    view_manager.register_view("RACE_WEEKEND", race_view)
    
    # Start on Dashboard
    view_manager.transition_to("DASHBOARD")

    clock = pygame.time.Clock()
    is_running = True
    
    while is_running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            # Let the UI Manager handle generic input
            ui_manager.process_events(event)
            
            # Let the current view handle specific logic and return transition names
            if view_manager.current_view:
                next_view_name = view_manager.current_view.handle_event(event)
                if next_view_name:
                    view_manager.transition_to(next_view_name)

        # Update
        ui_manager.update(time_delta)
        if view_manager.current_view:
            view_manager.current_view.update(time_delta)

        # Draw
        if view_manager.current_view:
            view_manager.current_view.draw()
            
        ui_manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
