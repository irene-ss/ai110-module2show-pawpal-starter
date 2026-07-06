from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class Task:
    task_id: str
    title: str
    duration: int
    priority_level: PriorityLevel = PriorityLevel.MEDIUM
    owner_preferences: Optional[str] = None
    constraints: Optional[str] = None
    scheduled_time: Optional[datetime] = None

    def complete_task(self) -> None:
        """Mark the task as completed."""
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        pass

    def update_profile(self, name: Optional[str] = None, species: Optional[str] = None,
                       breed: Optional[str] = None, age: Optional[int] = None) -> None:
        """Update the pet's profile information."""
        pass


@dataclass
class Owner:
    owner_id: str
    name: str
    email: str
    phone: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def create_task(self, pet: Pet, title: str, duration: int, priority_level: PriorityLevel = PriorityLevel.MEDIUM,
                    owner_preferences: Optional[str] = None, constraints: Optional[str] = None) -> Task:
        """Create a new task for a pet."""
        pass

    def view_schedule(self) -> List[Task]:
        """Return the owner's scheduled tasks."""
        pass
