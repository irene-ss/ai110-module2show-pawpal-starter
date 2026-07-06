from datetime import datetime

from pawpal_system import Owner, Pet, PriorityLevel, Scheduler, Task, TaskStatus


def test_task_completion_changes_status():
    task = Task(task_id="t1", title="Feed cat", duration=10)

    task.mark_complete()

    assert task.status == TaskStatus.COMPLETED
    assert task.is_completed() is True


def test_task_addition_increases_pet_task_count():
    pet = Pet(pet_id="p1", name="Luna", species="Dog")
    task = Task(task_id="t2", title="Walk dog", duration=15, priority_level=PriorityLevel.HIGH)

    initial_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert task in pet.tasks


def test_recurring_task_creates_next_occurrence_when_completed():
    owner = Owner(owner_id="o1", name="Casey", email="casey@example.com")
    pet = Pet(pet_id="p2", name="Milo", species="Cat")
    owner.add_pet(pet)

    original_task = owner.create_task(
        pet=pet,
        title="Daily brush",
        duration=5,
        scheduled_time=datetime(2026, 7, 6, 9, 0),
        frequency="daily",
    )

    scheduler = Scheduler()
    scheduler.mark_task_complete(owner, original_task.task_id)

    assert original_task.status == TaskStatus.COMPLETED
    assert len(pet.tasks) == 2
    next_task = [task for task in pet.tasks if task.task_id != original_task.task_id][0]
    assert next_task.frequency == "daily"
    assert next_task.scheduled_time == datetime(2026, 7, 7, 9, 0)
