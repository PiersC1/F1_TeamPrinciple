# Simulators

The `simulators/` directory houses the math-heavy execution engines that run the core "gameplay" loop in a headless, deterministic manner.

## Key Simulators:
- **`race_simulator.py`**: The crown jewel of the backend. It takes an array of `RaceEntry` objects (combining a Driver, Car, and Tire Strategy) and a `Track` object. 
    It simulates a race lap-by-lap by calculating a base time from the track and car synergies, then modifying it with unpredictable variance, tire wear degradation, and pit stop logic based on the user's assigned strategy cue. It outputs a comprehensive `"race_log"` that the React frontend parses to physically animate the race playback.
