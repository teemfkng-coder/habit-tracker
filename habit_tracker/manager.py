from datetime import date
from typing import Optional, Tuple, List

from .habit import Habit
from .repository import HabitRepository
from .analytics import Analytics


class HabitManager:
    """
    High-level API used by the UI / notebook.

    It coordinates between the HabitRepository (SQLite) and Analytics.
    """

    def __init__(self, repo: Optional[HabitRepository] = None) -> None:
        self.repo = repo or HabitRepository()

    # -------- CRUD operations ---------------------------------------------

    def create_habit(self, name: str, description: str, periodicity: str) -> Habit:
        habit = Habit(name=name, description=description, periodicity=periodicity)
        return self.repo.add_habit(habit)

    def list_habits(
        self,
        periodicity: Optional[str] = None,
        active_only: bool = True,
    ) -> List[Habit]:
        habits = self.repo.list_habits(active_only=active_only)
        if periodicity:
            habits = [h for h in habits if h.periodicity == periodicity]
        return habits

    def list_by_period(self, periodicity: str) -> List[Habit]:
        return self.list_habits(periodicity=periodicity, active_only=True)

    def archive_habit(self, habit_id: int) -> None:
        self.repo.archive_habit(habit_id)

    def complete_habit(self, habit_id: int, when: Optional[date] = None) -> None:
        when = when or date.today()
        self.repo.save_completion(habit_id, when)

    def mark_completed(self, habit_id: int, when: Optional[date] = None) -> None:
        return self.complete_habit(habit_id, when)

    def get_completions(self, habit_id: int):
        """
        Return all completion dates for a habit.
        """
        return self.repo.get_completions(habit_id)


    # -------- Analytics helpers -------------------------------------------

    def streak_for_habit(self, habit_id: int) -> int:
        habit = self.repo.get_habit(habit_id)
        if habit is None:
            raise ValueError(f"No habit with id={habit_id}")
        completions = self.repo.get_completions(habit_id)
        return Analytics.compute_streak(habit, completions)

    def streak_overall(self) -> Optional[Tuple[Habit, int]]:
        """
        Return the habit with the highest current streak and the streak length.
        """
        habits = self.repo.list_habits(active_only=True)
        if not habits:
            return None

        best_habit: Optional[Habit] = None
        best_streak = -1

        for habit in habits:
            completions = self.repo.get_completions(habit.id)
            streak = Analytics.compute_streak(habit, completions)
            if streak > best_streak:
                best_streak = streak
                best_habit = habit

        if best_habit is None:
            return None

        return best_habit, best_streak
