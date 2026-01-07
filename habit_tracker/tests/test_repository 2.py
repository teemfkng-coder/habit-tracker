from habit_tracker.repository import HabitRepository
from habit_tracker.habit import Habit


def test_add_and_list_habits(tmp_path):
    db_path = tmp_path / "test.db"
    repo = HabitRepository(db_path=db_path)

    habit = Habit(
        name="Test Habit",
        description="Demo habit",
        periodicity="daily",
    )
    repo.add_habit(habit)

    habits = repo.list_habits()
    assert len(habits) == 1

    h = habits[0]
    assert h.id is not None
    assert h.name == "Test Habit"
    assert h.description == "Demo habit"
    assert h.periodicity == "daily"
    assert h.archived is False


def test_save_and_get_completions(tmp_path):
    db_path = tmp_path / "test.db"
    repo = HabitRepository(db_path=db_path)

    habit = Habit(
        name="Skill Practice",
        description="",
        periodicity="daily",
    )
    repo.add_habit(habit)

    repo.save_completion(habit.id, "2025-01-01")
    repo.save_completion(habit.id, "2025-01-02")

    completions = repo.get_completions(habit.id)

    # newest first
    assert completions == ["2025-01-02", "2025-01-01"]
