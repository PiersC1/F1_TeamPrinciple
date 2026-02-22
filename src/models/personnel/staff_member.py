from typing import Dict, Any
import uuid

class StaffMember:
    """Base class for all team personnel (Drivers, Tech Directors, etc.)."""
    
    def __init__(self, name: str, salary: int, rating: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.salary = salary
        self.rating = rating # 1-100 overall skill representation

    def to_dict(self) -> Dict[str, Any]:
        """Serialize core attributes for save/load. Subclasses should call this and extend."""
        return {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "rating": self.rating
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StaffMember':
        """Deserialize core attributes. Subclasses should override and use this."""
        member = cls(
            name=data["name"],
            salary=data["salary"],
            rating=data["rating"]
        )
        member.id = data["id"]
        return member
