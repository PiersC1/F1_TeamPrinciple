# Database

The `database/` directory contains static data definitions that populate the game world on initialization. 

## Key Files:
- **`market_database.py`**: Defines the initial pool of available Free Agents (Drivers and leading Engineers) that teams can hire from.
- **`team_database.py`**: Defines the starting 10 teams on the grid, including their budgets, car stats, and starting driver pairings.
- **`track_database.py`**: Contains the hardcoded 24-race official F1 calendar, including specific characteristics for each track (e.g., Aero Weight vs Powertrain Weight) that dynamically react with car stats in the simulator.
- **`rd_tree.json`**: A massive JSON object defining the 37+ nodes in the Research & Development dependency graph, their costs, and their physical aero/chassis/powertrain stat payouts.
