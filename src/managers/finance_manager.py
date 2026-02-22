from typing import Dict, Any

class FinanceManager:
    """Manages the team's balance and adherence to the cost cap."""
    
    def __init__(self, initial_budget: int = 140_000_000, cost_cap: int = 140_000_000):
        self.balance = initial_budget
        self.cost_cap = cost_cap
        self.spent_under_cap = 0 # Track how much of the balance spent counts towards the cap
        
    def spend(self, amount: int, counts_towards_cap: bool = True) -> bool:
        """
        Attempts to spend money. 
        Returns True if successful, False if insufficient funds or it breaches the cap.
        """
        if amount > self.balance:
            print("Insufficient funds!")
            return False
            
        if counts_towards_cap and (self.spent_under_cap + amount) > self.cost_cap:
            print("Warning: This would breach the cost cap!")
            return False
            
        self.balance -= amount
        if counts_towards_cap:
            self.spent_under_cap += amount
            
        return True
        
    def add_funds(self, amount: int):
        """Adds funds to the balance (e.g., from sponsorships/prize money)."""
        self.balance += amount
        
    def cheat_set_cost_cap(self, new_cap: int):
        """Cheat menu function to alter the cost cap mid-game."""
        self.cost_cap = new_cap
        
    def cheat_add_funds(self, amount: int):
        """Cheat menu function to add infinite money."""
        self.balance += amount

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for save/load."""
        return {
            "balance": self.balance,
            "cost_cap": self.cost_cap,
            "spent_under_cap": self.spent_under_cap
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinanceManager':
        """Deserialize from save/load."""
        manager = cls(
            initial_budget=data.get('balance', 140_000_000), 
            cost_cap=data.get('cost_cap', 140_000_000)
        )
        manager.spent_under_cap = data.get('spent_under_cap', 0)
        return manager
