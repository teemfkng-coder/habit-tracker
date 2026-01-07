from habit_tracker.analytics import Analytics
from habit_tracker.habit import Habit


def test_daily_streak_continuous():
    habit = Habit(name="Daily Test", description="", periodicity="daily")
    completions = ["2025-01-01", "2025-01-02", "2025-01-03"]

    streak = Analytics.compute_streak(habit, completions)

    assert streak == 3


def test_daily_streak_broken():
    habit = Habit(name="Daily Test", description="", periodicity="daily")
    # missing 2025-01-04 breaks the streak
    completions = ["2025-01-03", "2025-01-05"]

    streak = Analytics.compute_streak(habit, completions)

    assert streak == 1


def test_weekly_streak():
    habit = Habit(name="Weekly Test", description="", periodicity="weekly")
    completions = ["2025-01-01", "2025-01-08", "2025-01-15"]

    streak = Analytics.compute_streak(habit, completions)

    assert streak == 3


def test_streak_empty_completion_list():
    habit = Habit(name="Empty", description="", periodicity="daily")
    completions = []

    streak = Analytics.compute_streak(habit, completions)

    assert streak == 0
