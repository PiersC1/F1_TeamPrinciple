from typing import Dict, Any, List
from src.models.car.rd_node import RDNode
from src.models.car.car import Car

class RDManager:
    """
    Manages the overall R&D tree, checking availability of nodes based on dependencies,
    processing time progression, and applying stats to the Car.
    """
    
    def __init__(self, car: Car):
        self.car = car
        self.nodes: Dict[str, RDNode] = {}
        self.active_project: RDNode | None = None
        
        self._initialize_default_tree()

    def _initialize_default_tree(self):
        """Hardcodes the initial tree for the MVP. We can load this from JSON later."""
        # 1. Base Aero Node
        n1 = RDNode("aero_b1", "Concept Aero", "Baseline aerodynamic testing in the wind tunnel.", cost=2_000_000, time_to_complete=2, effects={"aero.downforce": 5})
        n1.state = "AVAILABLE" # Root node
        
        # 2. Advanced Aero (Requires n1)
        n2 = RDNode("aero_adv", "High Downforce Concept", "Aggressive wing angles.", cost=5_000_000, time_to_complete=4, effects={"aero.downforce": 15, "aero.drag_efficiency": -5})
        n2.add_dependency("aero_b1")
        
        # 3. Efficient Aero (Requires n1, Mutually Exclusive with n2)
        n3 = RDNode("aero_eff", "Low Drag Concept", "Slippery design. Great for straights, bad in corners.", cost=5_000_000, time_to_complete=4, effects={"aero.downforce": -5, "aero.drag_efficiency": 15})
        n3.add_dependency("aero_b1")
        
        n2.add_mutually_exclusive("aero_eff")
        n3.add_mutually_exclusive("aero_adv")
        
        # 4. Heavy Powertrain (Tradeoff showcase)
        n4 = RDNode("powertrain_power", "Aggressive Engine Mapping", "Huge power, reduces reliability and adds weight for cooling.", cost=8_000_000, time_to_complete=3, effects={"powertrain.power_output": 20, "powertrain.reliability": -10, "chassis.weight_reduction": -5})
        n4.state = "AVAILABLE"

        for node in [n1, n2, n3, n4]:
            self.nodes[node.node_id] = node

    def update_availability(self):
        """Iterates through nodes and unlocks them if dependencies are met."""
        for node in self.nodes.values():
            if node.state == "LOCKED":
                # Check if all dependencies are COMPLETED
                deps_met = all(self.nodes[dep].state == "COMPLETED" for dep in node.dependencies)
                if deps_met:
                    node.state = "AVAILABLE"

    def start_project(self, node_id: str) -> bool:
        """Attempts to start an R&D project."""
        if self.active_project is not None:
            print("Already researching a project!")
            return False
            
        node = self.nodes.get(node_id)
        if not node or node.state != "AVAILABLE":
            return False
            
        node.state = "IN_PROGRESS"
        self.active_project = node
        
        # Lock out mutually exclusive options
        for ex_id in node.mutually_exclusive:
            if ex_id in self.nodes:
                self.nodes[ex_id].state = "MUTUALLY_LOCKED"
                
        return True

    def advance_time(self, time_units: int = 1):
        """Advances the active project by the given time units."""
        if not self.active_project:
            return
            
        self.active_project.progress_time += time_units
        if self.active_project.progress_time >= self.active_project.base_time_to_complete:
            self._complete_project(self.active_project)

    def _complete_project(self, node: RDNode):
        """Applies the effects of a completed node to the car."""
        node.state = "COMPLETED"
        print(f"R&D Completed: {node.name}")
        
        for stat_path, value in node.effects.items():
            self._apply_effect(stat_path, value)
            
        self.active_project = None
        self.update_availability() # Unlock subsequent tree nodes
        
    def _apply_effect(self, stat_path: str, value_change: int):
        """Reflection hack to easily apply paths like 'aero.downforce' to the Car object."""
        try:
            category, stat = stat_path.split('.')
            module = getattr(self.car, category) # e.g., self.car.aero
            current_val = getattr(module, stat)
            setattr(module, stat, current_val + value_change)
            print(f"  Applied [{stat_path}]: {value_change}")
        except Exception as e:
            print(f"Error applying R&D effect {stat_path}: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for save file."""
        return {
            "active_project": self.active_project.node_id if self.active_project else None,
            "nodes": [node.to_dict() for node in self.nodes.values()]
        }
        
    def load_from_dict(self, data: Dict[str, Any]):
        """Deserialize state from save file."""
        if not data:
            return
            
        for node_data in data.get("nodes", []):
            node_id = node_data["node_id"]
            if node_id in self.nodes:
                self.nodes[node_id].load_from_dict(node_data)
                
        active_id = data.get("active_project")
        if active_id and active_id in self.nodes:
            self.active_project = self.nodes[active_id]
