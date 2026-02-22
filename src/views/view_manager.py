from typing import Dict
from src.views.base_view import BaseView

class ViewManager:
    """Handles transitioning between different screens/views."""
    
    def __init__(self):
        self.views: Dict[str, BaseView] = {}
        self.current_view: BaseView | None = None
        
    def register_view(self, name: str, view: BaseView):
        self.views[name] = view
        
    def transition_to(self, name: str):
        if name not in self.views:
            print(f"Error: View '{name}' not found.")
            return
            
        if self.current_view:
            self.current_view.on_exit()
            
        self.current_view = self.views[name]
        self.current_view.on_enter()
