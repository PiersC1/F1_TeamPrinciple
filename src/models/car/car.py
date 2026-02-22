from typing import Dict, Any
from src.models.car.aerodynamics import Aerodynamics
from src.models.car.chassis import Chassis
from src.models.car.powertrain import Powertrain

class Car:
    """The aggregate Car model combining Aero, Chassis, and Powertrain."""
    
    def __init__(self):
        self.aero = Aerodynamics()
        self.chassis = Chassis()
        self.powertrain = Powertrain()
        
    def get_overall_performance(self) -> int:
        """Calculates a rough overall performance rating for basic UI display."""
        total = (self.aero.downforce + self.aero.drag_efficiency +
                 self.chassis.weight_reduction + self.chassis.tire_preservation +
                 self.powertrain.power_output + self.powertrain.reliability)
        return total // 6

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aero": self.aero.to_dict(),
            "chassis": self.chassis.to_dict(),
            "powertrain": self.powertrain.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Car':
        car = cls()
        if "aero" in data:
            car.aero = Aerodynamics.from_dict(data["aero"])
        if "chassis" in data:
            car.chassis = Chassis.from_dict(data["chassis"])
        if "powertrain" in data:
            car.powertrain = Powertrain.from_dict(data["powertrain"])
        return car
