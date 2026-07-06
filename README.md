# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

The implementation is organized across these project files:

- [app.py](app.py) — interactive Streamlit interface for entering tasks and viewing the schedule.
- [pawpal_system.py](pawpal_system.py) — core classes for Task, Pet, Owner, and Scheduler.
- [tests/test_pawpal.py](tests/test_pawpal.py) — pytest coverage for core scheduling behaviors.
- [diagrams/uml_final.mmd](diagrams/uml_final.mmd) — updated Mermaid UML diagram.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Run the app

```bash
streamlit run app.py
```

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

OUTPUT:
Today's Schedule
====================
- Morning walk | Pet: pet1 | Time: 08:00 | Priority: HIGH
- Feed dinner | Pet: pet1 | Time: 18:00 | Priority: MEDIUM
- Clean litter box | Pet: pet2 | Time: 20:00 | Priority: LOW

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover the core scheduler behaviors for PawPal+, including sorting tasks in chronological order, confirming that completing a daily task creates the next day's occurrence, and detecting conflicts when multiple tasks share the same scheduled time.

TESTING OUTPUT:
=============== test session starts ================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\rekha\OneDrive\Desktop\CodePath\AI 101\week 5 proj2\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 6 items                                   

tests\test_pawpal.py ......                   [100%]

================ 6 passed in 0.05s =================
SYSTEM RELIABILITY: 4.5 stars

## 📐 Smarter Scheduling

The scheduler now supports a few lightweight but useful behaviors for organizing pet care tasks.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Sorts tasks by their scheduled time so the day is displayed in chronological order. |
| Priority-based ordering | `Scheduler.organize_tasks()` | Orders tasks by priority, then time, then title for a structured plan. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when multiple tasks are assigned to the same scheduled time. |
| Recurring task logic | `Task.create_next_occurrence()` and `Scheduler.mark_task_complete()` | Automatically creates the next occurrence of daily or weekly tasks after one is completed. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status and/or pet name to focus on a specific subset of the schedule. |

## 📸 Demo Walkthrough

The Streamlit UI presents a simple pet care planner with an owner and pet profile section, task entry controls, and a schedule preview panel. Users can add tasks with a title, duration, and priority, then generate a sorted schedule and inspect any overlapping tasks.

A typical workflow looks like this:

1. Enter owner and pet details in the top form.
2. Add a care task by naming it, selecting duration, and choosing a priority level.
3. Review the live task table, which is automatically sorted by scheduled time.
4. Click “Generate schedule” to build a prioritized daily plan.
5. View conflict warnings if two tasks share the same scheduled time, and see recurring tasks appear after completion.

Key Scheduler behaviors shown in the app:

- Sorting by time and priority to display the most important tasks first.
- Conflict warnings when multiple tasks are scheduled at the same hour.
- Recurring task creation for daily or weekly tasks once they are completed.
- Filtering of pending tasks in the live schedule view.

Example CLI output from `main.py`:

```text
Today's Schedule
====================
- Morning walk | Pet: Mochi | Time: 08:00 | Priority: HIGH
- Feed dinner   | Pet: Mochi | Time: 12:00 | Priority: MEDIUM
- Evening meds  | Pet: Mochi | Time: 18:00 | Priority: LOW

Warning: tasks Morning walk, Feed dinner overlap at 08:00.
```
