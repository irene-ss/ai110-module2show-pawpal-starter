from pawpal_system import Pet, PriorityLevel, Task, TaskStatus


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
