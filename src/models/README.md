# Data Models

The `models/` directory contains the core object-oriented data structures that make up the game world. These are primarily pure state containers with minimal logic, designed to be easily serialized.

## Subdirectories:
- **`car/`**: Contains the `Car` object and its sub-modules (`Aerodynamics`, `Chassis`, `Powertrain`), as well as the specialized `TireCompound` and `RDNode` classes.
- **`personnel/`**: Contains the staff members (e.g., `Driver`, `TechnicalDirector`, `HeadOfAerodynamics`) which share a base `StaffMember` class that dictates aging and salaries.
- **`world/`**: Contains environmental models like the `Track` definitions for the racing calendar.

## Root Model:
- **`game_state.py`**: The god object. Holds the unified state of the player's team, the AI teams, the current UI state, and handles serialization/deserialization for the entire game loop.
