# Habit Tracker Application

## Overview

This project is a Python-based Habit Tracker developed as part of the Object-Oriented and Functional Programming with Python module.

- The application allows users to:
- Create and manage habits (daily or weekly)
- Persist habits and completion history using SQLite
- Track habit completions
- Compute streak analytics using pure, functional logic
- Validate correctness via automated tests

The design adheres to **Object-Oriented Programming (OOP)** principles, clearly separating concerns between persistence, domain logic, and analytics.

## Project Structure

```
habit_tracker/
├── habit_tracker/
│ ├── init.py
│ ├── habit.py # Habit domain model
│ ├── repository.py # SQLite persistence layer
│ ├── manager.py # Application-level API
│ ├── analytics.py # Pure analytics functions
│ └── data/
│ └── habits.db # SQLite database (auto-created)
│
├── tests/
│ ├── init.py
│ ├── test_repository.py
│ └── test_analytics.py
│
├── run_app.ipynb # Demonstration notebook
├── run_tests.ipynb # Test execution notebook
└── README.md
```

## Core Components
### 1. Habit (habit.py)

Represents a single habit with attributes such as:
- id
- name
- description
- periodicity (daily/weekly)
- created_at
- archived

### 2. HabitRepository (repository.py)

Handles all persistence using SQLite via Python’s built-in sqlite3 module:
- Creating tables
- Adding habits
- Archiving habits
- Saving completions
- Retrieving completion history

### 3. HabitManager (manager.py)

Acts as the high-level API used by the notebook or CLI:

- Create habits
- List habits
- Mark completions
- Retrieve completion history
- Compute streaks via analytics

### 4. Analytics (analytics.py)

Contains pure functional logic:

- No database access
- No side effects
- Deterministic streak computation for daily and weekly habits

## Running the Application

### Using the Notebook (Recommended)

1. Open Jupyter Lab

2. Navigate to the outer habit_tracker/ folder

3. Open run_app.ipynb

4. Run all cells top-to-bottom

The notebook demonstrates:

- Habit creation
- Listing habits
- Marking completions
- Viewing completion history
- Computing streak analytics

## Running Tests

### Using Terminal

- From the outer habit_tracker/ directory:

    pytest -q

### Using Notebook

- Open and run:

    run_tests.ipynb


All tests should pass locally.

## Analytics & Streak Rules

### Daily Habits

- A streak increases for each consecutive calendar day with a completion
- Missing a day breaks the streak

### Weekly Habits

- A streak increases for each consecutive week with at least one completion
- Skipping a week breaks the streak

Analytics functions are:

- Stateless
- Deterministic
- Fully test-covered

## Design Principles Applied

### 1.  Object-Oriented Programming

- Clear domain models
- Responsibility-driven classes

### 2. Functional Programming

- Pure analytics functions

### 3. Separation of Concerns

- Persistence, logic, and analytics are isolated

### 4. Testability

- Deterministic tests

- No hidden side effects

## Requirements

- Python 3.10+
- pytest
- sqlite3 (built-in)

## Author

**Tshireletso Moloi**
| Object-Oriented and Functional Programming with Python Module / 2025 