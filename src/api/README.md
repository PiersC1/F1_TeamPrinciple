# API Layer

The API layer is built using FastAPI. It acts as the bridge between the React frontend and the Python simulation engine.

## Key Files:
- **`main.py`**: The primary FastAPI application. It defines the REST endpoints for loading games, advancing time, simulating races, and interacting with the Staff Market. It maintains an in-memory instance of the `GameState` while the server is running.
