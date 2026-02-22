from typing import Dict, Any
from src.models.personnel.staff_member import StaffMember

class Driver(StaffMember):
    """Driver data model with specific performance attributes for the Simulator to use."""
    
    def __init__(self, name: str, salary: int, rating: int, speed: int, consistency: int, tire_management: int):
        super().__init__(name, salary, rating)
        self.speed = speed # Raw pace
        self.consistency = consistency # Ability to string together similar lap times
        self.tire_management = tire_management # Reduces tire wear per lap during simulation
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "speed": self.speed,
            "consistency": self.consistency,
            "tire_management": self.tire_management
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Driver':
        driver = cls(
            name=data.get("name", "Unknown Driver"),
            salary=data.get("salary", 5_000_000),
            rating=data.get("rating", 70),
            speed=data.get("speed", 70),
            consistency=data.get("consistency", 70),
            tire_management=data.get("tire_management", 70)
        )
        driver.id = data.get("id", driver.id)
        return driver
