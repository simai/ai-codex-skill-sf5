# Decision Policy

The coordinator must:

1. keep work inside SF5 scope;
2. choose the narrowest activity that explains the change;
3. avoid mixing upstream refresh, routing changes, and recipe work into one undocumented batch;
4. require validation for every routing, working-set, or validator change;
5. apply explicit gates from `rules/change-gates.md` for source refresh, working-set, and validation batches;
6. keep source-backed truth authoritative over memory or guesswork;
7. move speculative future improvements into remaining work rather than silently expanding the batch.

Escalate internally to a larger specialist set when:

- one change touches both source truth and routing;
- one change touches both routing and working-set generation;
- one change modifies generated artifacts and their validators;
- the task changes install surface or coordinator architecture.
