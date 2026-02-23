from typing import Dict, Any, List

class ChampionshipManager:
    """Tracks points for Drivers and Constructors across the season."""
    
    # Modern F1 points system (Top 10)
    POINTS_SYSTEM = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    
    def __init__(self):
        self.driver_standings: Dict[str, int] = {} # driver_name -> points
        self.constructor_standings: Dict[str, int] = {} # team_name -> points
        self.last_driver_champion: str = None
        self.last_constructor_champion: str = None
        
    def score_points(self, race_results: List[Dict[str, Any]]):
        """
        Takes the sorted 'standings' list from the RaceSimulator output and awards points.
        race_results format: [{"driver": name, "team": team_name, "total_time": X}, ...]
        """
        for position, result in enumerate(race_results):
            if position < len(self.POINTS_SYSTEM):
                points = self.POINTS_SYSTEM[position]
                driver = result["driver"]
                team = result["team"]
                
                # Award Driver Points
                if driver not in self.driver_standings:
                    self.driver_standings[driver] = 0
                self.driver_standings[driver] += points
                
                # Award Constructor Points
                if team not in self.constructor_standings:
                    self.constructor_standings[team] = 0
                self.constructor_standings[team] += points

    def get_sorted_driver_standings(self) -> List[tuple[str, int]]:
        return sorted(self.driver_standings.items(), key=lambda item: item[1], reverse=True)
        
    def get_sorted_constructor_standings(self) -> List[tuple[str, int]]:
        return sorted(self.constructor_standings.items(), key=lambda item: item[1], reverse=True)

    def end_season(self):
        """Calculates the champions, saves them, and clears current points for the next season."""
        driver_st = self.get_sorted_driver_standings()
        if driver_st:
            self.last_driver_champion = driver_st[0][0]
            
        team_st = self.get_sorted_constructor_standings()
        if team_st:
            self.last_constructor_champion = team_st[0][0]
            
        self.driver_standings = {}
        self.constructor_standings = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "driver_standings": self.driver_standings,
            "constructor_standings": self.constructor_standings,
            "last_driver_champion": self.last_driver_champion,
            "last_constructor_champion": self.last_constructor_champion
        }
        
    def load_from_dict(self, data: Dict[str, Any]):
        if not data:
            return
        self.driver_standings = data.get("driver_standings", {})
        self.constructor_standings = data.get("constructor_standings", {})
        self.last_driver_champion = data.get("last_driver_champion", None)
        self.last_constructor_champion = data.get("last_constructor_champion", None)
