from typing import Dict, Any

class Aerodynamics:
    """Aerodynamics module of the car. Affects downforce and drag."""
    
    def __init__(self, downforce: int = 50, drag_efficiency: int = 50):
        self.downforce = downforce # Higher is better cornering
        self.drag_efficiency = drag_efficiency # Higher means less drag, better top speed
        self.development_potential = 100 # cap to avoid infinite scaling
        
    def upgrade_downforce(self, amount: int):
        self.downforce = min(self.downforce + amount, self.development_potential)
        
    def upgrade_drag_efficiency(self, amount: int):
        self.drag_efficiency = min(self.drag_efficiency + amount, self.development_potential)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "downforce": self.downforce,
            "drag_efficiency": self.drag_efficiency
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Aerodynamics':
        return cls(
            downforce=data.get("downforce", 50),
            drag_efficiency=data.get("drag_efficiency", 50)
        )
