# React Components

The UI is broken down into thematic views, utilizing `lucide-react` for iconography and heavily relying on custom utility classes built with `Tailwind CSS` for styling.

## Major Views:
- **`Dashboard.jsx`**: The Main Hub. Displays the standings, active R&D pipeline progress, next race widget, and Team Financials.
- **`RaceWeekend.jsx`**: The Race screen. Handles pre-race Tire Strategy building and Post-Race Live Telemetry playback by parsing the `race_log` array over time.
- **`RDTree.jsx`**: The Tech Tree visualizer. Uses `@xyflow/react` to render a complex, interactive Directed Acyclic Graph (DAG) for panning, zooming, and initiating parts upgrades.
- **`StaffMarket.jsx`**: The HR portal. Displays the active staff roster alongside available Free Agents, allowing the calculation of severance and signing bonuses to poach new procedurally generated talent.
- **`MainMenu.jsx`**: The entry point. Handles parsing save files from the API or building custom data presets for a "New Game".
