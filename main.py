from datetime import datetime

from pawpal_system import Owner, Pet, PriorityLevel, Scheduler, TaskStatus


def main() -> None:
    owner = Owner(owner_id="owner1", name="Alex", email="alex@example.com")

    luna = Pet(pet_id="pet1", name="Luna", species="Dog", breed="Labrador", age=3)
    maxx = Pet(pet_id="pet2", name="Maxx", species="Cat", breed="Siamese", age=2)

    owner.add_pet(luna)
    owner.add_pet(maxx)

    owner.create_task(
        pet=maxx,
        title="Clean litter box",
        description="Clean Maxx's litter box",
        duration=15,
        priority_level=PriorityLevel.LOW,
        scheduled_time=datetime(2026, 7, 6, 20, 0),
    )

    owner.create_task(
        pet=luna,
        title="Morning walk",
        description="Take Luna for a walk",
        duration=20,
        priority_level=PriorityLevel.HIGH,
        scheduled_time=datetime(2026, 7, 6, 8, 0),
    )

    owner.create_task(
        pet=maxx,
        title="Feed Maxx",
        description="Feed Maxx at the same time as the walk",
        duration=10,
        priority_level=PriorityLevel.MEDIUM,
        scheduled_time=datetime(2026, 7, 6, 8, 0),
    )

    owner.create_task(
        pet=luna,
        title="Feed dinner",
        description="Feed Luna dinner",
        duration=10,
        priority_level=PriorityLevel.MEDIUM,
        scheduled_time=datetime(2026, 7, 6, 18, 0),
    )

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    pending_tasks = scheduler.filter_tasks(all_tasks, status=TaskStatus.PENDING, owner=owner)
    luna_tasks = scheduler.filter_tasks(all_tasks, pet_name="Luna", owner=owner)

    print("Sorted by time")
    print("=" * 20)
    for task in sorted_tasks:
        scheduled_time = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "Not set"
        print(f"- {task.title} | Pet: {task.pet_id} | Time: {scheduled_time}")

    print("\nPending tasks")
    print("=" * 20)
    for task in pending_tasks:
        print(f"- {task.title} ({task.status.value})")

    print("\nLuna's tasks")
    print("=" * 20)
    for task in luna_tasks:
        print(f"- {task.title}")

    print("\nConflict warnings")
    print("=" * 20)
    for warning in scheduler.detect_conflicts(all_tasks):
        print(f"- {warning}")


if __name__ == "__main__":
    main()