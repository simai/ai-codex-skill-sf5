# Specialist: routing-orchestrator

Owns scenarios, page recipe routing, pattern playbook routing, and fixture-backed route behavior.

Use when:

- top-level route selection changes;
- a query should resolve to a different scenario or recipe;
- route fixtures or ranking rules need updates.

Focus:

- keep routing deterministic;
- prefer explicit fixture coverage over intuition;
- separate mixed-intent cases with the smallest stable scoring rule.
