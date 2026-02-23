from typing import Dict, Any
from src.models.personnel.department_lead import DepartmentLead

class HeadOfAerodynamics(DepartmentLead):
    """Lead tracking aerodynamic-specific parts to boost their quality."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HeadOfAerodynamics':
        # Leverage the parent class's deserialization and cast to this type
        lead = DepartmentLead.from_dict(data)
        # Create a new instance of HeadOfAerodynamics
        aero = cls(
            name=lead.name,
            salary=lead.salary,
            rating=lead.rating,
            expertise=lead.expertise,
            age=lead.age,
            contract_length_years=lead.contract_length_years
        )
        aero.id = lead.id
        return aero
