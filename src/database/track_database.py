from typing import List
from src.models.world.track import Track

class TrackDatabase:
    """Hardcoded 10-race calendar with varying characteristics for MVP."""
    
    @staticmethod
    def get_calendar() -> List[Track]:
        return [
            # 1. Bahrain - Balanced
            Track("Bahrain International Circuit", "Bahrain", laps=57, base_lap_time=93.0, 
                  aero_weight=1.0, chassis_weight=1.0, powertrain_weight=1.0),
            
            # 2. Jeddah - High Speed, low downforce
            Track("Jeddah Corniche Circuit", "Saudi Arabia", laps=50, base_lap_time=89.0, 
                  aero_weight=0.8, chassis_weight=1.0, powertrain_weight=1.3),
                  
            # 3. Monaco - Max Downforce, Powertrain useless
            Track("Circuit de Monaco", "Monaco", laps=78, base_lap_time=72.0, 
                  aero_weight=1.5, chassis_weight=1.2, powertrain_weight=0.4),
                  
            # 4. Silverstone - High Speed aero
            Track("Silverstone Circuit", "Great Britain", laps=52, base_lap_time=87.0, 
                  aero_weight=1.3, chassis_weight=1.0, powertrain_weight=1.1),
                  
            # 5. Spa - Power and Aero Efficiency
            Track("Circuit de Spa-Francorchamps", "Belgium", laps=44, base_lap_time=105.0, 
                  aero_weight=1.1, chassis_weight=0.9, powertrain_weight=1.4),
                  
            # 6. Monza - Pure Power, minimum downforce
            Track("Autodromo Nazionale Monza", "Italy", laps=53, base_lap_time=81.0, 
                  aero_weight=0.5, chassis_weight=1.0, powertrain_weight=1.5),
                  
            # 7. Singapore - High Downforce, harsh on tires/chassis
            Track("Marina Bay Street Circuit", "Singapore", laps=62, base_lap_time=91.0, 
                  aero_weight=1.4, chassis_weight=1.3, powertrain_weight=0.6),
                  
            # 8. Suzuka - Extremely balanced, high chassis demand
            Track("Suzuka International Racing Course", "Japan", laps=53, base_lap_time=90.0, 
                  aero_weight=1.2, chassis_weight=1.3, powertrain_weight=1.0),
                  
            # 9. Interlagos - High Altitude (less power), good aero needed
            Track("Autodromo Jose Carlos Pace", "Brazil", laps=71, base_lap_time=71.0, 
                  aero_weight=1.1, chassis_weight=1.1, powertrain_weight=0.8),
                  
            # 10. Abu Dhabi - Stop-Start, traction (Chassis/Powertrain)
            Track("Yas Marina Circuit", "UAE", laps=58, base_lap_time=85.0, 
                  aero_weight=1.0, chassis_weight=1.2, powertrain_weight=1.2)
        ]
