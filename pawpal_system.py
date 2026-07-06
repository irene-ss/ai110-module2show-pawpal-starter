from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class Task:
    task_id: str
    title: str
    description: str = ""
    duration: int = 15
    scheduled_time: Optional[datetime] = None
    frequency: str = "one-time"
    priority_level: PriorityLevel = PriorityLevel.MEDIUM
    owner_preferences: Optional[str] = None
    constraints: Optional[str] = None
    pet_id: Optional[str] = None
    owner_id: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

    def __post_init__(self) -> None:
        """Validate task fields during initialization."""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty.")
        if self.duration < 0:
            raise ValueError("Duration must be non-negative.")
        self.frequency = self.frequency.lower()

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED

    def create_next_occurrence(self, pet: Optional[Pet] = None, owner: Optional[Owner] = None) -> Optional["Task"]:
        """Create the next occurrence of a recurring task."""
        if self.frequency not in {"daily", "weekly"}:
            return None

        if self.scheduled_time is None:
            return None

        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(days=7)
        next_scheduled_time = self.scheduled_time + delta

        if pet is None or owner is None:
            return None

        next_task = Task(
            task_id=f"{owner.owner_id}-{pet.pet_id}-{len(pet.tasks) + 1}",
            title=self.title,
            description=self.description,
            duration=self.duration,
            scheduled_time=next_scheduled_time,
            frequency=self.frequency,
            priority_level=self.priority_level,
            owner_preferences=self.owner_preferences,
            constraints=self.constraints,
            pet_id=pet.pet_id,
            owner_id=owner.owner_id,
        )
        pet.add_task(next_task)
        return next_task

    def is_completed(self) -> bool:
        """Return whether the task has been completed."""
        return self.status == TaskStatus.COMPLETED

    def to_summary(self) -> str:
        """Return a short human-readable summary of the task."""
        return f"{self.title} ({self.priority_level.value})"


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate pet age during initialization."""
        if self.age is not None and self.age < 0:
            raise ValueError("Age must be non-negative.")

    def add_task(self, task: Task) -> bool:
        """Add a task to the pet's task list if it is not already present."""
        if any(existing.task_id == task.task_id for existing in self.tasks):
            return False
        self.tasks.append(task)
        task.pet_id = self.pet_id
        return True

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the pet by its ID."""
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Return the pet's tasks, optionally filtered by status."""
        if status is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.status == status]

    def update_profile(self, name: Optional[str] = None, species: Optional[str] = None,
                       breed: Optional[str] = None, age: Optional[int] = None) -> None:
        """Update the pet's profile information."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if breed is not None:
            self.breed = breed
        if age is not None:
            if age < 0:
                raise ValueError("Age must be non-negative.")
            self.age = age


@dataclass
class Owner:
    owner_id: str
    name: str
    email: str
    phone: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> bool:
        """Add a pet to the owner's profile if it is not already registered."""
        if any(existing.pet_id == pet.pet_id for existing in self.pets):
            return False
        self.pets.append(pet)
        return True

    def create_task(self, pet: Pet, title: str, description: str = "", duration: int = 15,
                    priority_level: PriorityLevel = PriorityLevel.MEDIUM,
                    owner_preferences: Optional[str] = None, constraints: Optional[str] = None,
                    scheduled_time: Optional[datetime] = None, frequency: str = "one-time") -> Task:
        """Create a new task for a pet and register it with the owner."""
        if pet not in self.pets:
            self.add_pet(pet)

        task_id = f"{self.owner_id}-{pet.pet_id}-{len(pet.tasks) + 1}"
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            duration=duration,
            scheduled_time=scheduled_time,
            frequency=frequency,
            priority_level=priority_level,
            owner_preferences=owner_preferences,
            constraints=constraints,
            pet_id=pet.pet_id,
            owner_id=self.owner_id,
        )
        pet.add_task(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks belonging to the owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Return all tasks for a specific pet owned by this owner."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return list(pet.tasks)
        return []

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks for the owner's pets."""
        return [task for task in self.get_all_tasks() if not task.is_completed()]

    def view_schedule(self) -> List[Task]:
        """Return the owner's scheduled tasks."""
        return self.get_all_tasks()


@dataclass
class Scheduler:
    def retrieve_tasks(self, owner: Owner) -> List[Task]:
        """Retrieve all tasks from the owner's pets."""
        return owner.get_all_tasks()

    def organize_tasks(self, owner: Owner, include_completed: bool = False) -> List[Task]:
        """Return tasks sorted by priority and scheduled time."""
        tasks = self.retrieve_tasks(owner)
        if not include_completed:
            tasks = [task for task in tasks if not task.is_completed()]

        return sorted(
            tasks,
            key=lambda task: (
                self._priority_rank(task.priority_level),
                task.scheduled_time or datetime.max,
                task.title.lower(),
            ),
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled time for a simple daily view."""
        return sorted(tasks, key=lambda task: (task.scheduled_time or datetime.max, task.title.lower()))

    def filter_tasks(self, tasks: List[Task], *, status: Optional[TaskStatus] = None, pet_name: Optional[str] = None, owner: Optional[Owner] = None) -> List[Task]:
        """Filter tasks by completion status or pet name."""
        filtered_tasks = list(tasks)
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]
        if pet_name is not None:
            filtered_tasks = [
                task for task in filtered_tasks
                if self._pet_name_for_task(task, owner) == pet_name
            ]
        return filtered_tasks

    def mark_task_complete(self, owner: Owner, task_id: str) -> bool:
        """Mark a task complete if it exists in the owner's schedule."""
        for task in self.retrieve_tasks(owner):
            if task.task_id == task_id:
                task.mark_complete()
                if task.frequency in {"daily", "weekly"}:
                    pet = next((pet for pet in owner.pets if pet.pet_id == task.pet_id), None)
                    task.create_next_occurrence(pet=pet, owner=owner)
                return True
        return False

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return lightweight warnings for overlapping scheduled tasks."""
        grouped_tasks: dict[datetime, List[Task]] = {}
        for task in tasks:
            if task.scheduled_time is None:
                continue
            grouped_tasks.setdefault(task.scheduled_time, []).append(task)

        warnings: List[str] = []
        for scheduled_time, grouped in grouped_tasks.items():
            if len(grouped) > 1:
                conflict_tasks = ", ".join(task.title for task in grouped)
                warnings.append(
                    f"Warning: tasks {conflict_tasks} overlap at {scheduled_time.strftime('%H:%M')}."
                )

        return warnings

    def _priority_rank(self, priority_level: PriorityLevel) -> int:
        ranking = {
            PriorityLevel.HIGH: 0,
            PriorityLevel.MEDIUM: 1,
            PriorityLevel.LOW: 2,
        }
        return ranking[priority_level]

    def _pet_name_for_task(self, task: Task, owner: Optional[Owner]) -> str:
        """Return the pet name for a task when available."""
        if owner is None:
            return "Unknown"
        for pet in owner.pets:
            if pet.pet_id == task.pet_id:
                return pet.name
        return "Unknown"
