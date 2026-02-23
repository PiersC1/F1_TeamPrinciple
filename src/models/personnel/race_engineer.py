from typing import Dict, Any
from src.models.personnel.staff_member import StaffMember

class RaceEngineer(StaffMember):
    """Assigned 1:1 with a driver. A high-rating Race Engineer can mitigate consistency or tire wear penalties during races."""
    
    def __init__(self, name: str, salary: int, rating: int, age: int = 35, contract_length_years: int = 2):
        super().__init__(name, salary, rating, age, contract_length_years)
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RaceEngineer':
        member = StaffMember.from_dict(data)
        engineer = cls(
            name=member.name,
            salary=member.salary,
            rating=member.rating,
            age=member.age,
            contract_length_years=member.contract_length_years
        )
        engineer.id = member.id
        return engineer
