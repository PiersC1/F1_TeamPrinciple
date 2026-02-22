import pygame
import pygame_gui
from src.models.game_state import GameState

class BaseView:
    """Interface for all screens in the game."""
    def __init__(self, manager: pygame_gui.UIManager, game_state: GameState, window_surface: pygame.Surface):
        self.ui_manager = manager
        self.game_state = game_state
        self.window_surface = window_surface
        self.is_active = False

    def on_enter(self):
        """Called when transitioning TO this view. Setup UI elements here."""
        self.is_active = True

    def on_exit(self):
        """Called when transitioning AWAY from this view. Teardown UI elements here."""
        self.is_active = False
        self.ui_manager.clear_and_reset()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle events. Return the string name of the next view to transition to, or None."""
        return None

    def update(self, delta_time: float):
        """Update logic per frame."""
        pass

    def draw(self):
        """Draw everything behind the UI manager."""
        pass
