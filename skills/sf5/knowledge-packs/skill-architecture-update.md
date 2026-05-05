# Knowledge Pack: Skill Architecture Update

Use this pack when the activity is `skill-architecture-update`.

Focus:

- coordinator model
- activity manifests
- specialist profiles
- metadata and entrypoint consistency

Default artifacts:

- `SKILL.md`
- `activities/*.json`
- `specialists/*/profile.md`
- `rules/*.md`
- `quality/*.md`
- `agents/openai.yaml`

Minimum verification:

- activity manifests parse as JSON;
- key entrypoints reference the new coordinator model consistently;
- local checks stay green after structural changes.
