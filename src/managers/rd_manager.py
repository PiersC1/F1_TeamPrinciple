import os
import json
from typing import Dict, Any, List
from src.models.car.rd_node import RDNode
from src.models.car.car import Car

class RDManager:
    """
    Manages the overall R&D tree, checking availability of nodes based on dependencies,
    processing time progression, and applying stats to the Car.
    """
    
    def __init__(self, car: Car, is_ai: bool = False):
        self.car = car
        self.is_ai = is_ai
        self.difficulty = "Normal" # "Easy", "Normal", "Hard" (Only affects AI)
        self.resource_points: int = 500
        self.total_engineers: int = 100
        self.nodes: Dict[str, RDNode] = {}
        self.active_projects: Dict[str, int] = {} # Dict mapping node_id -> number of allocated engineers
        
        self.head_of_aero = None      # Will be set by GameState
        self.powertrain_lead = None   # Will be set by GameState
        self._initialize_default_tree()

    def _initialize_default_tree(self):
        """Loads the defined research tree from the database JSON file."""
        # Find path to the database relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "database", "rd_tree.json")
        
        try:
            with open(json_path, 'r') as f:
                tree_data = json.load(f)
                
            for node_data in tree_data:
                node = RDNode(
                    node_id=node_data["id"],
                    name=node_data["name"],
                    description=node_data["description"],
                    rp_cost=node_data.get("rp_cost", 100),
                    base_workload=node_data.get("base_workload", 200),
                    effects=node_data["effects"]
                )
                
                # Add dependencies
                for dep in node_data.get("requires", []):
                    node.add_dependency(dep)
                    
                # Store mutually exclusive lockouts
                for lock in node_data.get("locks_out", []):
                    node.add_mutually_exclusive(lock)
                    
                # If no dependencies, it's a starting node
                if not node.dependencies:
                    node.state = "AVAILABLE"
                    
                self.nodes[node.node_id] = node
                
        except Exception as e:
            print(f"Error loading R&D json tree: {e}")

    def update_availability(self):
        """Iterates through nodes and unlocks them if dependencies are met."""
        available_nodes = []
        for node in self.nodes.values():
            if node.state == "LOCKED":
                # Check if all dependencies are COMPLETED
                deps_met = all(self.nodes[dep].state == "COMPLETED" for dep in node.dependencies)
                if deps_met:
                    node.state = "AVAILABLE"
            if node.state == "AVAILABLE":
                available_nodes.append(node)
                
        # Autonomous AI logic
        if self.is_ai and available_nodes:
            self._auto_select_project(available_nodes)
            
    def _auto_select_project(self, available_nodes: List[RDNode]):
        """AI picks projects if they have RP and assigns remaining engineers."""
        import random
        # Try to start a new project if we have funds
        if self.resource_points > 100:
            affordable = [n for n in available_nodes if self.resource_points >= n.rp_cost]
            if affordable:
                choice = random.choice(affordable)
                self.start_project(choice.node_id)
                
        # Allocate any free engineers to active projects
        free_engineers = self.total_engineers - sum(self.active_projects.values())
        if free_engineers > 0 and self.active_projects:
            # Just dump them all into a random active project
            target_id = random.choice(list(self.active_projects.keys()))
            self.allocate_engineers(target_id, self.active_projects[target_id] + free_engineers)

    def allocate_engineers(self, node_id: str, new_amount: int) -> bool:
        """Assigns a specific number of engineers to an active project."""
        if node_id not in self.active_projects:
            return False
            
        current_amount = self.active_projects[node_id]
        total_allocated = sum(self.active_projects.values())
        
        # Calculate how many unassigned engineers we have, ignoring the ones already on this project
        free_engineers = self.total_engineers - (total_allocated - current_amount)
        
        if new_amount > free_engineers:
            return False
            
        self.active_projects[node_id] = new_amount
        return True

    def start_project(self, node_id: str, bypass_funds: bool = False) -> bool:
        """Attempts to purchase an R&D project with Resource Points."""
        node = self.nodes.get(node_id)
        if not node or node.state != "AVAILABLE":
            return False
            
        if not bypass_funds:
            if self.resource_points < node.rp_cost:
                return False
            self.resource_points -= node.rp_cost
            
        node.state = "IN_PROGRESS"
        self.active_projects[node_id] = 0 # Initially 0 engineers assigned
        
        if self.is_ai:
            print(f"[{'AI'}] purchased project: {node.name}")
        
        # Lock out mutually exclusive options
        for ex_id in node.mutually_exclusive:
            if ex_id in self.nodes:
                self.nodes[ex_id].state = "MUTUALLY_LOCKED"
                
        self.update_availability()
        return True

    def advance_time(self, time_units: int = 1):
        """Advances active projects based on assigned engineers. 1 time_unit = 1 Race."""
        completed_this_tick = []
        
        for node_id, engineers in self.active_projects.items():
            node = self.nodes[node_id]
            
            # Difficulty modifier for AI AI baseline engineers effectively do more or less work
            effective_engineers = engineers
            if self.is_ai:
                if self.difficulty.lower() == "easy":
                    effective_engineers = int(effective_engineers * 0.75) # 25% slower
                elif self.difficulty.lower() == "hard":
                    effective_engineers = int(effective_engineers * 1.25) # 25% faster
            
            node.invested_work += (effective_engineers * time_units)
            
            if node.invested_work >= node.base_workload:
                completed_this_tick.append(node_id)
                
        for completed_id in completed_this_tick:
            self._complete_project(self.nodes[completed_id])

    def _complete_project(self, node: RDNode):
        """Applies the effects of a completed node to the car, including Department Head bonuses."""
        node.state = "COMPLETED"
        print(f"R&D Completed: {node.name}")
        
        # Remove from active queue
        if node.node_id in self.active_projects:
            del self.active_projects[node.node_id]
        
        for stat_path, value in node.effects.items():
            bonus = 0
            # Apply Department Head Synergy Bonuses dynamically
            if stat_path.startswith("aero.") and self.head_of_aero:
                bonus = self.head_of_aero.get_rd_bonus()
            elif stat_path.startswith("powertrain.") and self.powertrain_lead:
                bonus = self.powertrain_lead.get_rd_bonus()
                
            # If the value is negative (a tradeoff), don't boost the negative effect.
            # E.g. Downforce +10, Drag -5. We want Downforce +15, Drag -5.
            if value > 0:
                self._apply_effect(stat_path, value + bonus)
                if bonus > 0:
                    print(f"  (Department Synergy Bonus: +{bonus})")
            else:
                self._apply_effect(stat_path, value)
            
        self.update_availability() # Unlock subsequent tree nodes
        
    def _apply_effect(self, stat_path: str, value_change: int):
        """Reflection hack to easily apply paths like 'aero.downforce' to the Car object."""
        try:
            category, stat = stat_path.split('.')
            module = getattr(self.car, category) # e.g., self.car.aero
            current_val = getattr(module, stat)
            
            # Clamp limits. If they hit 100 on the old system, let them push to 150+ now.
            new_val = current_val + value_change
            setattr(module, stat, new_val)
            print(f"  Applied [{stat_path}]: {value_change}")
        except Exception as e:
            print(f"Error applying R&D effect {stat_path}: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for save file."""
        return {
            "is_ai": self.is_ai,
            "difficulty": self.difficulty,
            "resource_points": self.resource_points,
            "total_engineers": self.total_engineers,
            "active_projects": self.active_projects,
            "nodes": [node.to_dict() for node in self.nodes.values()]
        }
        
    def load_from_dict(self, data: Dict[str, Any]):
        """Deserialize state from save file."""
        if not data:
            return
            
        self.is_ai = data.get("is_ai", False)
        self.difficulty = data.get("difficulty", "Normal")
        self.resource_points = data.get("resource_points", 500)
        self.total_engineers = data.get("total_engineers", 100)
        self.active_projects = data.get("active_projects", {})
            
        for node_data in data.get("nodes", []):
            node_id = node_data["node_id"]
            if node_id in self.nodes:
                self.nodes[node_id].load_from_dict(node_data)
