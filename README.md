# F1 Team Principal Simulator

A fully decoupled, mathematically-driven Formula 1 management simulator.

## Architecture

The project is split into two distinct halves:
1. **Backend (`src/`)**: A stateless Python simulation and REST API powered by FastAPI.
2. **Frontend (`frontend/`)**: A React + Vite web dashboard styled with Tailwind CSS.

## Features Currently Implemented

*   **24-Race Calendar**: A full simulation of the official 2024 calendar with track-specific characteristics (Aero, Chassis, Powertrain demands).
*   **Dynamic Race Engine**: The python backend simulates a 50+ lap race tracking tire degradation, pace variance, and pit strategy execution.
*   **Live Telemetry Playback**: Watch the race unfold in real-time in the React dashboard with speed controls.
*   **R&D Tech Tree**: Manage a staff of 100 engineers across a 37-node dependency graph to upgrade your car's physical downforce, weight, and engine power.
*   **Staff Market**: Poach Drivers, Technical Directors, Aero Leads, and Powertrain Leads from a dynamic Free Agent pool using your budget.
*   **Multi-Season Support**: Compete for the Constructors' Championship, earn End-of-Season Prize Money based on your grid position, and advance into future years against fully autonomous AI teams.

## Getting Started

1. Set up your Python environment and start the backend server:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```
2. In a new terminal, start the Vite frontend development server:
```bash
cd frontend
npm install
npm run dev
```
