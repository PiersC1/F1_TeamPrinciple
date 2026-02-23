# Source Code (Backend)

The `src` directory contains the core logic, simulation engine, and API for the F1 Team Principal game. The backend is built in Python 3.10+ using FastAPI and Pydantic for data validation.

## Architecture

The backend is completely decoupled from the frontend, operating as an autonomous simulation engine that is controlled via state mutations over REST API endpoints.

- **`api/`**: Contains the FastAPI application and REST endpoints.
- **`models/`**: The core data structures of the game (e.g., `Car`, `Driver`, `GameState`).
- **`managers/`**: Stateful controller classes that mutate models (e.g., `FinanceManager`, `RDManager`).
- **`simulators/`**: The math-heavy execution engines (e.g., `RaceSimulator`).
- **`database/`**: Static game data (e.g., the 24-race calendar, R&D tree, initial team rosters).
- **`utils/`**: Helper scripts like the `SaveLoadManager` for writing states to disk.
