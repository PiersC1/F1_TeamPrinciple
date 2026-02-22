from typing import Dict, Any

class Powertrain:
    """Powertrain module of the car. Affects acceleration and reliability."""
    
    def __init__(self, power_output: int = 50, reliability: int = 80):
        self.power_output = power_output # Overall engine horsepower
        self.reliability = reliability # Chance of mechanical DNF (higher is better)
        self.development_potential = 100
        
    def upgrade_power(self, amount: int):
        self.power_output = min(self.power_output + amount, self.development_potential)
        
    def upgrade_reliability(self, amount: int):
        self.reliability = min(self.reliability + amount, self.development_potential)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "power_output": self.power_output,
            "reliability": self.reliability
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Powertrain':
        return cls(
            power_output=data.get("power_output", 50),
            reliability=data.get("reliability", 80)
        )
