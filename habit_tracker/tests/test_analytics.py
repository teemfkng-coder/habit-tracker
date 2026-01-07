from habit_tracker.analytics import Analytics
from habit_tracker.habit import Habit


def test_daily_streak_continuous():
    habit = Habit(name="Daily Test", description="", periodicity="daily")
    completions = ["2025-01-05", "2025-01-04", "2025-01-03", "2025-01-02"]

    streak = Analytics.compute_streak(habit, completions)
    assert streak == 4


def test_daily_streak_broken():
    habit = Habit(name="Daily Test", description="", periodicity="daily")
    completions = ["2025-01-05", "2025-01-03", "2025-01-02"]

    streak = Analytics.compute_streak(habit, completions)
    assert streak == 1


def test_weekly_streak():
    habit = Habit(name="Weekly Check-in", description="", periodicity="weekly")
    completions = ["2025-01-22", "2025-01-15", "2025-01-08"]

    streak = Analytics.compute_streak(habit, completions)
    assert streak == 3
