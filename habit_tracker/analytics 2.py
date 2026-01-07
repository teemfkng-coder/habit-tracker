from datetime import datetime, timedelta
from typing import Sequence

from .habit import Habit


class Analytics:
    """
    Pure logic for computing streaks and other statistics.
    """

    @staticmethod
    def compute_streak(habit: Habit, completions: Sequence[str]) -> int:
        """
        Compute the **current streak** for a habit.

        Parameters
        ----------
        habit : Habit
            Habit with periodicity "daily" or "weekly".
        completions : sequence of str
            ISO date strings "YYYY-MM-DD".

        Returns
        -------
        int
            Number of consecutive periods up to the most recent completion.
        """
        if not completions:
            return 0

        # unique dates, sorted descending
        dates = sorted(
            {datetime.fromisoformat(d).date() for d in completions},
            reverse=True,
        )

        current = dates[0]
        streak = 1

        step = timedelta(days=1) if habit.periodicity == "daily" else timedelta(weeks=1)

        for d in dates[1:]:
            if d == current - step:
                streak += 1
                current = d
            else:
                break

        return streak
