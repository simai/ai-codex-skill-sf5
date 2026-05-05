# Output Contract

For every substantial SF5 task, return:

1. Goal and `Done when` if the task is not trivial.
2. Selected activity and the specialist set when the work crosses several surfaces.
3. Layer mapping or surface mapping for the implementation decision.
4. Changed artifacts or generated outputs.
5. Verification result or an explicit reason verification could not run.
6. Remaining required work and optional follow-up.

For non-trivial work, prefer this compact internal matrix:

| Specialist | Role | Scope | Blocking |
|---|---|---|---|
| validation-qa | reviewer, gatekeeper | checks and regressions | yes |

When the task changes routing, source-backed data, recipes, or generated bundles, verification is mandatory unless a real blocker exists.
