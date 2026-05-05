# Specialist Engagement Model

Use explicit specialist roles when the task crosses more than one SF5 surface.

Allowed roles:

- `author`
- `reviewer`
- `gatekeeper`
- `consulted`

Default role bias:

- `task-goal`: `author`, `gatekeeper`
- `skill-maintainer`: `author`, `gatekeeper`
- `source-sync`: `author`, `reviewer`
- `routing-orchestrator`: `author`, `reviewer`
- `recipe-scaffold`: `author`
- `working-set`: `author`, `reviewer`
- `validation-qa`: `reviewer`, `gatekeeper`
- `docs-learning`: `author`, `reviewer`

Use explicit gatekeepers when:

- source-backed truth is refreshed
- routing behavior changes
- fixtures or validators change
- generated bundle contracts change
- the skill architecture itself is being refactored
