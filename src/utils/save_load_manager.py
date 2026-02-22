import json
import os
from typing import Dict, Any

class SaveLoadManager:
    """Handles serializing the GameState to and from JSON format."""
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_game(self, slot_name: str, state_data: Dict[str, Any]) -> bool:
        """Saves a dictionary representing the game state to a JSON file."""
        filepath = os.path.join(self.save_dir, f"{slot_name}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(state_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot_name: str) -> Dict[str, Any]:
        """Loads a game state dictionary from a JSON file. Returns empty dict if not found."""
        filepath = os.path.join(self.save_dir, f"{slot_name}.json")
        if not os.path.exists(filepath):
            return {}
            
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return {}

    def get_save_slots(self) -> list[str]:
        """Returns a list of available save slot names."""
        if not os.path.exists(self.save_dir):
            return []
        
        slots = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith(".json"):
                slots.append(filename[:-5])
        return slots
