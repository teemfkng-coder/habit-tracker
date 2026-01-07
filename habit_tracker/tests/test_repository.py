import pytest

from habit_tracker.habit import Habit
from habit_tracker.repository import HabitRepository


@pytest.fixture()
def repository(tmp_path):
    """Creates a fresh SQLite DB per test run."""
    db_path = tmp_path / "test_habits.db"
    return HabitRepository(db_path=str(db_path))


def test_add_and_list_habits(repository):
    habit = Habit(name="Test Habit", description="Test desc", periodicity="daily")
    habit_id = repository.add_habit(habit)

    habits = repository.list_habits()

    assert len(habits) >= 1
    assert any(h.id == habit_id for h in habits)
    assert any(h.name == "Test Habit" for h in habits)


def test_save_and_get_completions(repository):
    habit = Habit(name="Daily Habit", description="", periodicity="daily")
    habit_id = repository.add_habit(habit)

    repository.save_completion(habit_id, "2025-01-01")
    repository.save_completion(habit_id, "2025-01-02")

    completions = repository.get_completions(habit_id)

    assert "2025-01-01" in completions
    assert "2025-01-02" in completions


def test_archive_habit(repository):
    """
    Soft-delete / archive a habit and confirm it no longer appears in the default list.
    """
    habit = Habit(name="Archive Me", description="", periodicity="weekly")
    habit_id = repository.add_habit(habit)

    # archive it
    repository.archive_habit(habit_id)

    # Default behaviour: archived habits should not appear
    habits = repository.list_habits()
    assert all(h.id != habit_id for h in habits)


def test_list_active_vs_archived(repository):
    """
    Confirm you can retrieve archived items when explicitly requested.
    """
    habit = Habit(name="Visible When Archived", description="", periodicity="daily")
    habit_id = repository.add_habit(habit)
    repository.archive_habit(habit_id)

    # active list should not show it
    active = repository.list_habits()
    assert all(h.id != habit_id for h in active)

    # archived-inclusive list SHOULD show it
    all_habits = repository.list_habits(include_archived=True)
    assert any(h.id == habit_id for h in all_habits)
