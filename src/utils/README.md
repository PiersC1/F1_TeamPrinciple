# Utils

The `utils/` directory contains helper scripts and backend infrastructure that don't directly model gameplay mechanics.

## Key Utilities:
- **`save_load_manager.py`**: An atomic I/O utility that reads and writes the massive, nested `GameState` dictionary to JSON files in the `saves/` root directory, enabling campaign persistence across server restarts.
