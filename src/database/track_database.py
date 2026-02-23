from typing import List
from src.models.world.track import Track

class TrackDatabase:
    """Hardcoded 10-race calendar with varying characteristics for MVP."""
    
    @staticmethod
    def get_calendar() -> List[Track]:
        return [
            # 1. Bahrain
            Track("Bahrain International Circuit", "Bahrain", laps=57, base_lap_time=93.0, 
                  aero_weight=1.0, chassis_weight=1.0, powertrain_weight=1.0),
            # 2. Saudi Arabia
            Track("Jeddah Corniche Circuit", "Saudi Arabia", laps=50, base_lap_time=89.0, 
                  aero_weight=0.8, chassis_weight=1.0, powertrain_weight=1.3),
            # 3. Australia
            Track("Albert Park Circuit", "Australia", laps=58, base_lap_time=81.0, 
                  aero_weight=0.9, chassis_weight=1.1, powertrain_weight=1.0),
            # 4. Japan
            Track("Suzuka International Racing Course", "Japan", laps=53, base_lap_time=90.0, 
                  aero_weight=1.2, chassis_weight=1.3, powertrain_weight=1.0),
            # 5. China
            Track("Shanghai International Circuit", "China", laps=56, base_lap_time=96.0, 
                  aero_weight=1.1, chassis_weight=1.1, powertrain_weight=1.0),
            # 6. Miami
            Track("Miami International Autodrome", "USA", laps=57, base_lap_time=90.0, 
                  aero_weight=0.9, chassis_weight=1.0, powertrain_weight=1.2),
            # 7. Imola
            Track("Autodromo Enzo e Dino Ferrari", "Italy", laps=63, base_lap_time=77.0, 
                  aero_weight=1.0, chassis_weight=1.2, powertrain_weight=1.0),
            # 8. Monaco
            Track("Circuit de Monaco", "Monaco", laps=78, base_lap_time=72.0, 
                  aero_weight=1.5, chassis_weight=1.2, powertrain_weight=0.4),
            # 9. Canada
            Track("Circuit Gilles-Villeneuve", "Canada", laps=70, base_lap_time=73.0, 
                  aero_weight=0.7, chassis_weight=1.1, powertrain_weight=1.3),
            # 10. Spain
            Track("Circuit de Barcelona-Catalunya", "Spain", laps=66, base_lap_time=76.0, 
                  aero_weight=1.2, chassis_weight=1.1, powertrain_weight=0.9),
            # 11. Austria
            Track("Red Bull Ring", "Austria", laps=71, base_lap_time=66.0, 
                  aero_weight=0.9, chassis_weight=1.0, powertrain_weight=1.3),
            # 12. Great Britain
            Track("Silverstone Circuit", "Great Britain", laps=52, base_lap_time=87.0, 
                  aero_weight=1.3, chassis_weight=1.0, powertrain_weight=1.1),
            # 13. Hungary
            Track("Hungaroring", "Hungary", laps=70, base_lap_time=79.0, 
                  aero_weight=1.3, chassis_weight=1.2, powertrain_weight=0.7),
            # 14. Belgium
            Track("Circuit de Spa-Francorchamps", "Belgium", laps=44, base_lap_time=105.0, 
                  aero_weight=1.1, chassis_weight=0.9, powertrain_weight=1.4),
            # 15. Netherlands
            Track("Circuit Zandvoort", "Netherlands", laps=72, base_lap_time=72.0, 
                  aero_weight=1.3, chassis_weight=1.1, powertrain_weight=0.8),
            # 16. Italy (Monza)
            Track("Autodromo Nazionale Monza", "Italy", laps=53, base_lap_time=81.0, 
                  aero_weight=0.5, chassis_weight=1.0, powertrain_weight=1.5),
            # 17. Azerbaijan
            Track("Baku City Circuit", "Azerbaijan", laps=51, base_lap_time=103.0, 
                  aero_weight=0.6, chassis_weight=0.9, powertrain_weight=1.4),
            # 18. Singapore
            Track("Marina Bay Street Circuit", "Singapore", laps=62, base_lap_time=91.0, 
                  aero_weight=1.4, chassis_weight=1.3, powertrain_weight=0.6),
            # 19. USA (Austin)
            Track("Circuit of the Americas", "USA", laps=56, base_lap_time=95.0, 
                  aero_weight=1.1, chassis_weight=1.1, powertrain_weight=1.0),
            # 20. Mexico
            Track("Autodromo Hermanos Rodriguez", "Mexico", laps=71, base_lap_time=80.0, 
                  aero_weight=0.9, chassis_weight=1.1, powertrain_weight=1.0),
            # 21. Brazil
            Track("Autodromo Jose Carlos Pace", "Brazil", laps=71, base_lap_time=71.0, 
                  aero_weight=1.1, chassis_weight=1.1, powertrain_weight=0.8),
            # 22. Las Vegas
            Track("Las Vegas Strip Circuit", "USA", laps=50, base_lap_time=93.0, 
                  aero_weight=0.6, chassis_weight=0.8, powertrain_weight=1.5),
            # 23. Qatar
            Track("Lusail International Circuit", "Qatar", laps=57, base_lap_time=84.0, 
                  aero_weight=1.2, chassis_weight=1.1, powertrain_weight=0.9),
            # 24. Abu Dhabi
            Track("Yas Marina Circuit", "UAE", laps=58, base_lap_time=85.0, 
                  aero_weight=1.0, chassis_weight=1.2, powertrain_weight=1.2)
        ]
