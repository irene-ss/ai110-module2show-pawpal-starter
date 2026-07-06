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
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status and/or pet name to focus on a specific subset of the schedule. |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when multiple tasks are assigned to the same scheduled time. |
| Recurring task logic | `Task.create_next_occurrence()` and `Scheduler.mark_task_complete()` | Automatically creates the next occurrence of daily or weekly tasks after one is completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
