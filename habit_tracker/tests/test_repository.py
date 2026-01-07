import pytest

from habit_tracker.habit import Habit
from habit_tracker.repository import HabitRepository


@pytest.fixture
def repository(tmp_path):
    """Fresh repository + fresh DB for every test."""
    db_path = tmp_path / "habits.db"
    return HabitRepository(str(db_path))


def _add(repo: HabitRepository, name: str, periodicity: str = "daily") -> Habit:
    """Create a habit and ensure it has a valid integer id."""
    habit = Habit(name=name, description="Test desc", periodicity=periodicity)

    result = repo.add_habit(habit)

    # Your repo might return an int id OR return the Habit back with id set.
    if isinstance(result, int):
        habit.id = result
        return habit

    if isinstance(result, Habit):
        return result

    # If add_habit returns None, assume it mutated the original habit.
    return habit


def _hid(h: Habit) -> int:
    assert hasattr(h, "id") and isinstance(h.id, int), "Habit id was not set correctly."
    return h.id


def test_add_and_list_habits(repository):
    _add(repository, name="Test Habit", periodicity="daily")

    habits = repository.list_habits()

    assert len(habits) >= 1
    assert any(h.name == "Test Habit" and h.periodicity == "daily" for h in habits)


def test_save_and_get_completions(repository):
    h = _add(repository, name="Daily Walk", periodicity="daily")
    hid = _hid(h)

    repository.save_completion(hid, "2025-01-01")
    repository.save_completion(hid, "2025-01-02")

    completions = repository.get_completions(hid)

    # DB ordering can differ; make the test deterministic
    assert sorted(completions) == ["2025-01-01", "2025-01-02"]


def test_empty_completion_list(repository):
    h = _add(repository, name="No Completions Yet", periodicity="daily")
    completions = repository.get_completions(_hid(h))

    assert completions == []


def test_archive_habit(repository):
    h_active = _add(repository, name="Active Habit", periodicity="daily")
    h_archived = _add(repository, name="Archived Habit", periodicity="weekly")

    repository.archive_habit(_hid(h_archived))

    habits = repository.list_habits()

    # Default list should only show active habits
    assert any(h.name == "Active Habit" for h in habits)
    assert all(h.name != "Archived Habit" for h in habits)
