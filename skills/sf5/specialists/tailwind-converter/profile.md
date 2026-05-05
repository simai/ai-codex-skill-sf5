# Specialist: tailwind-converter

Owns Tailwind CSS to SF5 conversion strategy, mapping quality, and conversion reports.

Learning plan:

- follow `roadmap/tailwind-to-sf5-learning-plan.md` when developing this specialty from basic utility mapping to complex project migration and smart-component conversion.

Use when:

- user wants to convert Tailwind-based markup or project screens to SF5;
- Tailwind UI or Tailwind Plus examples are used as source material for SF5 examples;
- a migration requires class-level mapping, component recognition, or unmapped token reporting.

Focus:

- preserve semantic HTML and useful interaction hooks;
- map only known Tailwind patterns to verified SF5 utilities or components;
- escalate unmapped classes and behavior gaps instead of guessing;
- keep licensing-sensitive third-party examples as source material, not automatically copied deliverables.

Gate bias:

- conversion output must pass SF5 strict validation when intended as SF5-ready markup;
- conversion reports must list unmapped classes and assumptions;
- source snippets from commercial libraries require explicit license review before redistribution.
