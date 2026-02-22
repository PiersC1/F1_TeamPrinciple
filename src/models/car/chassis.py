from typing import Dict, Any

class Chassis:
    """Chassis module of the car. Affects weight and tire wear."""
    
    def __init__(self, weight_reduction: int = 50, tire_preservation: int = 50):
        self.weight_reduction = weight_reduction # Higher means lighter car, better overall pace
        self.tire_preservation = tire_preservation # Higher means tires last longer
        self.development_potential = 100
        
    def upgrade_weight_reduction(self, amount: int):
        self.weight_reduction = min(self.weight_reduction + amount, self.development_potential)
        
    def upgrade_tire_preservation(self, amount: int):
        self.tire_preservation = min(self.tire_preservation + amount, self.development_potential)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "weight_reduction": self.weight_reduction,
            "tire_preservation": self.tire_preservation
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chassis':
        return cls(
            weight_reduction=data.get("weight_reduction", 50),
            tire_preservation=data.get("tire_preservation", 50)
        )
