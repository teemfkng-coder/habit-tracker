from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional


@dataclass
class Habit:
    """
    Represents a single habit.

    Attributes
    ----------
    id : Optional[int]
        Unique identifier (primary key in the DB).
    name : str
        Short name, e.g. "Document one learning".
    description : str
        Optional longer explanation.
    periodicity : str
        "daily" or "weekly".
    created_at : datetime
        Timestamp when the habit was created.
    archived : bool
        Flag to mark habits that are no longer active.
    """

    name: str
    description: str
    periodicity: str  # "daily" or "weekly"
    created_at: datetime = field(default_factory=datetime.utcnow)
    archived: bool = False
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if self.periodicity not in {"daily", "weekly"}:
            raise ValueError("periodicity must be 'daily' or 'weekly'")
