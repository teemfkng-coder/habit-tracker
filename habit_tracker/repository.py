import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional

from .habit import Habit

# Project root = .../Submissions/habit_tracker
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_DB_PATH = DATA_DIR / "habits.db"


class HabitRepository:
    """Handles all SQLite operations for habits and completions."""

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self._ensure_db()

    # --- internal helpers -------------------------------------------------

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_db(self) -> None:
        """Create tables if they do not exist."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    archived INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
                )
                """
            )
            conn.commit()

    def _row_to_habit(self, row: tuple) -> Habit:
        id_, name, description, periodicity, created_at, archived = row
        return Habit(
            id=id_,
            name=name,
            description=description or "",
            periodicity=periodicity,
            created_at=datetime.fromisoformat(created_at),
            archived=bool(archived),
        )

    # --- habit methods -----------------------------------------------------

    def add_habit(self, habit: Habit) -> Habit:
        """Insert a new habit into the DB and return it with id set."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO habits (name, description, periodicity, created_at, archived)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    habit.name,
                    habit.description,
                    habit.periodicity,
                    habit.created_at.isoformat(),
                    int(habit.archived),
                ),
            )
            habit_id = cur.lastrowid
            conn.commit()

        habit.id = habit_id
        return habit

    def list_habits(self, active_only: bool = True) -> List[Habit]:
        """Return all habits, optionally only active ones."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            if active_only:
                cur.execute(
                    """
                    SELECT id, name, description, periodicity, created_at, archived
                    FROM habits
                    WHERE archived = 0
                    ORDER BY id
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT id, name, description, periodicity, created_at, archived
                    FROM habits
                    ORDER BY id
                    """
                )
            rows = cur.fetchall()

        return [self._row_to_habit(row) for row in rows]

    def get_habit(self, habit_id: int) -> Optional[Habit]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, name, description, periodicity, created_at, archived
                FROM habits
                WHERE id = ?
                """,
                (habit_id,),
            )
            row = cur.fetchone()

        return self._row_to_habit(row) if row else None

    def archive_habit(self, habit_id: int) -> None:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE habits SET archived = 1 WHERE id = ?", (habit_id,))
            conn.commit()

    # --- completion methods -----------------------------------------------

    def save_completion(self, habit_id: int, completed_at: date | datetime | str) -> None:
        """Store a completion for a habit on a specific day."""
        if isinstance(completed_at, (date, datetime)):
            completed_str = completed_at.strftime("%Y-%m-%d")
        else:
            completed_str = str(completed_at)

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO completions (habit_id, completed_at)
                VALUES (?, ?)
                """,
                (habit_id, completed_str),
            )
            conn.commit()

    def get_completions(self, habit_id: int) -> List[str]:
        """
        Return completion dates as a list of ISO date strings, newest first.
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT completed_at
                FROM completions
                WHERE habit_id = ?
                ORDER BY completed_at DESC
                """,
                (habit_id,),
            )
            rows = cur.fetchall()

        return [r[0] for r in rows]
