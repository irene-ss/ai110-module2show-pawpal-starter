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


def test_sort_by_time_orders_tasks_chronologically():
    scheduler = Scheduler()
    later_task = Task(task_id="t3", title="Evening walk", scheduled_time=datetime(2026, 7, 6, 18, 0))
    earlier_task = Task(task_id="t4", title="Morning feed", scheduled_time=datetime(2026, 7, 6, 8, 0))
    middle_task = Task(task_id="t5", title="Afternoon meds", scheduled_time=datetime(2026, 7, 6, 12, 0))

    ordered_tasks = scheduler.sort_by_time([later_task, earlier_task, middle_task])

    assert [task.task_id for task in ordered_tasks] == ["t4", "t5", "t3"]


def test_marking_daily_task_complete_creates_next_day_task():
    owner = Owner(owner_id="o2", name="Taylor", email="taylor@example.com")
    pet = Pet(pet_id="p3", name="Mochi", species="Dog")
    owner.add_pet(pet)

    task = owner.create_task(
        pet=pet,
        title="Daily potty break",
        duration=10,
        scheduled_time=datetime(2026, 7, 8, 7, 30),
        frequency="daily",
    )

    scheduler = Scheduler()
    scheduler.mark_task_complete(owner, task.task_id)

    created_tasks = [candidate for candidate in pet.tasks if candidate.task_id != task.task_id]
    assert len(created_tasks) == 1
    assert created_tasks[0].scheduled_time == datetime(2026, 7, 9, 7, 30)


def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler()
    task_one = Task(task_id="t6", title="Feed pet", scheduled_time=datetime(2026, 7, 6, 9, 0))
    task_two = Task(task_id="t7", title="Walk pet", scheduled_time=datetime(2026, 7, 6, 9, 0))

    warnings = scheduler.detect_conflicts([task_one, task_two])

    assert len(warnings) == 1
    assert "Feed pet" in warnings[0]
    assert "Walk pet" in warnings[0]
