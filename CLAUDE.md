# Personal Copilot Assistant - Claude Instructions

## Purpose

This is a general-purpose assistant workspace. Use it for tasks not connected to specific websites or projects.

---

## Filing Schema

### `tasks/` — Active & Completed Work
Work items for tasks that don't belong to other repos.

| Folder | Purpose |
|--------|---------|
| `tasks/active/` | Currently running tasks |
| `tasks/archived/` | Completed or stalled tasks |
| `tasks/templates/` | Reusable task templates |

**Naming**: `YYYY-MM-DD-short-description.md`

### `memories/user/` — Persistent User Knowledge
Long-lived facts about the user.

| File | Purpose |
|------|---------|
| `memories/user/profile.md` | Identity, preferences, habits |
| `memories/user/projects.md` | Active projects and their status |
| `memories/user/contacts.md` | People and their contexts |
| `memories/user/links.md` | Frequently used URLs and resources |
| `memories/user/patterns.md` | Coding/work patterns that work for user |
| `memories/user/...` | Add more topic files as needed |

### `memories/session/` — Temporary Session Notes
Current conversation context. Auto-cleaned after session.

| File | Purpose |
|------|---------|
| `memories/session/current-task.md` | What we're working on now |
| `memories/session/plan.md` | Multi-step plan with checkboxes |
| `memories/session/context.md` | Background info for this session |

### `skills/` — Reusable Knowledge Packets
How to do specific things for this user.

**Naming**: `skill-name/SKILL.md`

Structure mirrors Copilot skill format:
- `skills/<domain>/SKILL.md` — Instructions
- `skills/<domain>/assets/` — Supporting files

---

## Working Principles

- Be proactive - don't wait to be asked for everything
- Use session memory to track multi-step tasks
- Store useful facts in user memory for future reference
- Prefer short, actionable responses

## Git Operations

- **Allowed**: `git status`, `git diff`, `git log`, `git show`, `git reflog`
- **Requires permission**: `git checkout`, `git reset`, `git push`, `git branch -d`

## Context Efficiency

- Context-aware delegation to subagents for complex multi-step tasks
- Use `runSubagent` for self-contained tasks that benefit from parallelization
- Keep responses concise - target 1-3 sentences for simple answers
