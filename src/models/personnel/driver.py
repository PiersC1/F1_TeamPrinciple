from typing import Dict, Any
from src.models.personnel.staff_member import StaffMember

class Driver(StaffMember):
    """Driver data model with specific performance attributes for the Simulator to use."""
    
    def __init__(self, name: str, salary: int, rating: int, speed: int, consistency: int, tire_management: int, age: int = 25, contract_length_years: int = 2):
        super().__init__(name, salary, rating, age, contract_length_years)
        self.speed = speed # Raw pace
        self.consistency = consistency # Ability to string together similar lap times
        self.tire_management = tire_management # Reduces tire wear per lap during simulation
        
    def process_weekly_aging(self):
        """Drivers develop speed fast when young, but maintain consistency later into their careers."""
        super().process_weekly_aging()
        import random
        
        # Determine dynamic stat growth or decline
        if self.age < 26.0:
            if random.random() < 0.05:
                self.speed = min(100, self.speed + 1)
            if random.random() < 0.03:
                self.tire_management = min(100, self.tire_management + 1)
        elif self.age > 33.0:
            if random.random() < 0.06:
                self.speed = max(1, self.speed - 1)
            # Consistency tends to hold on longer, maybe even goes up slightly in 30s
            if random.random() < 0.02:
                self.consistency = min(100, self.consistency + 1)
        
        if self.age > 38.0:
            # Drop off a cliff
            if random.random() < 0.1:
                self.consistency = max(1, self.consistency - 1)
                self.tire_management = max(1, self.tire_management - 1)
        
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
            tire_management=data.get("tire_management", 70),
            age=data.get("age", 25),
            contract_length_years=data.get("contract_length_years", 2)
        )
        driver.id = data.get("id", driver.id)
        return driver
