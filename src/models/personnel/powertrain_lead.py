from typing import Dict, Any
from src.models.personnel.department_lead import DepartmentLead

class PowertrainLead(DepartmentLead):
    """Lead tracking powertrain-specific parts to boost their quality."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PowertrainLead':
        lead = DepartmentLead.from_dict(data)
        powertrain = cls(
            name=lead.name,
            salary=lead.salary,
            rating=lead.rating,
            expertise=lead.expertise,
            age=lead.age,
            contract_length_years=lead.contract_length_years
        )
        powertrain.id = lead.id
        return powertrain
