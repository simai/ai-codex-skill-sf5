# Coordinator Gate Template

Use this gate for non-trivial SF5 skill work.

```json
{
  "goal": "Short goal statement",
  "activity": "routing-maintenance",
  "specialists": [
    {"name": "routing-orchestrator", "role": "author"},
    {"name": "validation-qa", "role": "gatekeeper"}
  ],
  "verdict": "approved_with_conditions",
  "blocking_findings": [],
  "required_before_done": [
    "run local checks",
    "update the matching fixture set"
  ],
  "remaining": [
    "optional follow-up item"
  ]
}
```
