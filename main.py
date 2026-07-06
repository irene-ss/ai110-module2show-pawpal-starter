from datetime import datetime

from pawpal_system import Owner, Pet, PriorityLevel, Scheduler


def main() -> None:
    owner = Owner(owner_id="owner1", name="Alex", email="alex@example.com")

    luna = Pet(pet_id="pet1", name="Luna", species="Dog", breed="Labrador", age=3)
    maxx = Pet(pet_id="pet2", name="Maxx", species="Cat", breed="Siamese", age=2)

    owner.add_pet(luna)
    owner.add_pet(maxx)

    owner.create_task(
        pet=luna,
        title="Morning walk",
        description="Take Luna for a walk",
        duration=20,
        priority_level=PriorityLevel.HIGH,
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

    owner.create_task(
        pet=maxx,
        title="Clean litter box",
        description="Clean Maxx's litter box",
        duration=15,
        priority_level=PriorityLevel.LOW,
        scheduled_time=datetime(2026, 7, 6, 20, 0),
    )

    scheduler = Scheduler()
    today_schedule = scheduler.organize_tasks(owner)

    print("Today's Schedule")
    print("=" * 20)
    for task in today_schedule:
        scheduled_time = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "Not set"
        print(f"- {task.title} | Pet: {task.pet_id} | Time: {scheduled_time} | Priority: {task.priority_level.value}")


if __name__ == "__main__":
    main()