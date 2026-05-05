# Specialist Assessment Template

Use this structure when several SF5 specialists are engaged.

```json
{
  "specialist": "routing-orchestrator",
  "role": "author, reviewer",
  "status": "approved_with_conditions",
  "summary": "Main conclusion in 1-2 sentences.",
  "findings": [
    {
      "severity": "medium",
      "issue": "Mixed RU/EN route still falls through to catalog-listing.",
      "recommendation": "Add fixture and a narrow ranking boost for the target scenario."
    }
  ],
  "acceptance": {
    "passed": false,
    "missing": [
      "route fixture",
      "local check confirmation"
    ]
  }
}
```
