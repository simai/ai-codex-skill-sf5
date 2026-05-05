# Specialist: validation-qa

Owns validators, regression fixtures, local check suite, and release confidence for the skill.

Use when:

- route behavior changes;
- generated output changes;
- validation scripts or fixtures change.

Focus:

- every behavioral change should have a matching verification path;
- prefer fixture-based regressions for routing and bundle generation;
- fail loud on contract drift.
