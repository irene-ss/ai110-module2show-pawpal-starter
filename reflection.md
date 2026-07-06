# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design focused on a simple pet care system with three main classes: Owner, Pet, and Task. The Owner class represents the person managing the pet care routine and is responsible for creating tasks and viewing the schedule. The Pet class represents an individual animal and is responsible for storing basic profile information and holding the tasks assigned to that pet. The Task class represents a specific care activity, such as feeding or walking, and stores details like duration, priority level, owner preferences, and constraints. I also included a PriorityLevel enum to represent task urgency. The overall design was meant to show how an owner can manage multiple pets and assign care tasks to each one in a structured way.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The AI feedback did point out some disparities so the updated design became slightly more structured during implementation. I added a TaskStatus enum so each task could clearly track whether it was still pending or completed, which made the task lifecycle easier to represent. This change was useful because it made the skeleton more realistic and reduced the chance of logic issues when creating or viewing tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers time, task priority, and task completion status. It uses scheduled_time to order tasks, priority_level to decide which tasks should appear earlier in the plan, and status to filter out completed tasks from the active schedule. I treated time and priority as the most important constraints because they directly affect whether a schedule is practical and helpful for the owner. Owner preferences and constraints were also included in the task model, but the current scheduler focuses mainly on the core scheduling signals that are easiest to validate in this version.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler currently checks for conflicts by looking for tasks scheduled at the exact same time, rather than detecting full overlap based on duration. This is reasonable for this project because the scheduler is lightweight and intended to provide simple warnings, not a full calendar engine. Focusing on exact time matches keeps the logic easier to understand and faster to run while still catching the most obvious scheduling conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
