from typing import Dict, Any
from src.models.personnel.staff_member import StaffMember

class TechnicalDirector(StaffMember):
    """Technical Director data model. Highly impacts R&D speed and cost efficiency."""
    
    def __init__(self, name: str, salary: int, rating: int, aero_expertise: int, chassis_expertise: int, powertrain_expertise: int):
        super().__init__(name, salary, rating)
        self.aero_expertise = aero_expertise
        self.chassis_expertise = chassis_expertise
        self.powertrain_expertise = powertrain_expertise
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "aero_expertise": self.aero_expertise,
            "chassis_expertise": self.chassis_expertise,
            "powertrain_expertise": self.powertrain_expertise
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TechnicalDirector':
        td = cls(
            name=data.get("name", "Unknown TD"),
            salary=data.get("salary", 1_000_000),
            rating=data.get("rating", 70),
            aero_expertise=data.get("aero_expertise", 70),
            chassis_expertise=data.get("chassis_expertise", 70),
            powertrain_expertise=data.get("powertrain_expertise", 70)
        )
        td.id = data.get("id", td.id)
        return td
