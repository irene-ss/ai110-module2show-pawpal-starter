import streamlit as st

from pawpal_system import Owner, Pet, PriorityLevel, Scheduler, TaskStatus

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="demo-owner", name=owner_name, email="demo@example.com")
owner = st.session_state.owner
owner.name = owner_name

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_id="demo-pet", name=pet_name, species=species)
pet = st.session_state.pet
pet.name = pet_name
pet.species = species
owner.add_pet(pet)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_level = {
        "low": PriorityLevel.LOW,
        "medium": PriorityLevel.MEDIUM,
        "high": PriorityLevel.HIGH,
    }[priority]
    owner.create_task(
        pet=pet,
        title=task_title,
        duration=int(duration),
        priority_level=priority_level,
    )
    st.success(f"Added '{task_title}' to {pet.name}'s schedule.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    scheduler = Scheduler()
    include_completed = st.checkbox("Include completed tasks in schedule view", value=False)
    visible_tasks = scheduler.filter_tasks(
        all_tasks,
        status=None if include_completed else TaskStatus.PENDING,
    )
    chronological_tasks = scheduler.sort_by_time(visible_tasks)

    st.write("Current tasks (sorted by time):")
    task_rows = [
        {
            "title": task.title,
            "pet": next((p.name for p in owner.pets if p.pet_id == task.pet_id), "Unknown"),
            "time": task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "Not set",
            "duration": task.duration,
            "priority": task.priority_level.value,
            "status": task.status.value,
        }
        for task in chronological_tasks
    ]
    st.table(task_rows)

    conflicts = scheduler.detect_conflicts(chronological_tasks)
    if conflicts:
        st.warning("Possible scheduling conflicts detected:")
        for conflict in conflicts:
            st.write(f"- {conflict}")
    else:
        st.success("No overlapping tasks detected for the visible schedule.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    organized_tasks = scheduler.organize_tasks(owner, include_completed=False)
    if organized_tasks:
        st.success("Schedule generated successfully.")
        st.table(
            [
                {
                    "title": task.title,
                    "pet": next((p.name for p in owner.pets if p.pet_id == task.pet_id), "Unknown"),
                    "time": task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "Not set",
                    "priority": task.priority_level.value,
                    "status": task.status.value,
                }
                for task in organized_tasks
            ]
        )

        conflicts = scheduler.detect_conflicts(organized_tasks)
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("The generated schedule has no overlapping tasks.")
    else:
        st.info("No tasks available to schedule yet.")
