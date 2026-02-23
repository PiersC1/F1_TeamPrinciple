# Managers

The `managers/` directory contains the active controller classes that perform logic and mutate the data models.

## Key Managers:
- **`finance_manager.py`**: Handles checking budgets, deducting costs, and processing End-of-Season prize money payouts.
- **`rd_manager.py`**: A complex parallel job scheduler. It tracks active engineering projects, accrues invested time (Resource Points), handles unlocking dependencies in the tech tree, and applies the physical stat bonuses to the attached `Car` model.
- **`championship_manager.py`**: A ledger that tallies race results into the official Driver and Constructor Standings and keeps track of historical champions.
