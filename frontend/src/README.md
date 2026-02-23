# React Frontend

The `frontend/` directory contains the modern web UI for the F1 Team Principal game, built using React, Vite, and Tailwind CSS.

## Architecture
The frontend is completely stateless regarding the simulation logic. It is purely a visualizer that renders the current JSON state representation periodically provided by the FastAPI server's `/api/state` endpoint. It issues command requests (like "Start R&D Project" or "Simulate Race") via HTTP POST back to the server to enact state mutations.

- **`components/`**: Modular React functional components that make up the views.
- **`assets/`**: Static files like the SVG icons for R&D Tree nodes.
- **`App.jsx`**: The root app component which handles basic manual routing between views and maintains the single global `gameState` object polling loop.
