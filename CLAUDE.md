# Personal Copilot Assistant - Claude Instructions

## Purpose

This is a general-purpose assistant workspace. Use it for tasks not connected to specific websites or projects.

## Memory Organization

| Scope | Path | Purpose |
|-------|------|---------|
| User memory | `/memories/user/` | Persistent notes across all workspaces |
| Session memory | `/memories/session/` | Task-specific temporary notes |

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
