# Specialist: bitrix-integration

Owns SF5 usage inside Bitrix modules and projects.

Use when:

- packaging SF5 UI assets into a Bitrix module or site starter;
- wiring `window.sfPath`, `window.sfSmartPath`, core CSS/JS, loader config, fonts, and icon behavior;
- creating installable demo pages under a Bitrix public path;
- validating that Bitrix runtime loads SF5 locally without CDN;
- aligning SF5 frontend packages with `simai.main`, `simai.data`, or other Bitrix project layers.

Focus:

- keep UI core and smart-components as separate versioned frontend packages;
- derive module payloads from release folders or archives without flattening versions;
- avoid mixing `ui-smart` files into ordinary `component/` assets;
- preserve Bitrix module ownership and uninstall markers;
- do not overwrite site-specific `simai.data` or unrelated `/simai/*` project folders during runtime sync;
- verify real Bitrix URLs with PHP lint, HTTP smoke, and browser/HAR evidence.

Default contract:

- `simai.ui/<version>/` contains core, loader, rules, components, utilities, fonts, and metadata.
- `simai.ui.smart/<version>/` contains a `smart/` directory with smart-component JS/CSS/template assets.
- `window.sfPath` points to the `simai.ui` version root.
- `window.sfSmartPath` points to the `simai.ui.smart` version root.
- Demo/example renderers read only whitelist manifests and never arbitrary query-string file paths.

Release intake:

- For a UI release like `ui-5.0.1`, copy only the distributable payload root that contains `core/`, `component/`, `utility/`, `rule/`, `fonts/` into `install/starter/simai/asset/simai.ui/<version>/`.
- For a smart release like `ui-smart-5.0.0`, copy the release `smart/` directory into `install/starter/simai/asset/simai.ui.smart/<version>/smart/`.
- Keep UI and smart versions independent. Do not force `simai.ui.smart` to match `simai.ui` unless the release actually has the same version.
- After replacing a version, update `window.sfPath`, `window.sfSmartPath`, demo labels, smoke URLs, and docs/release notes.

Acceptance:

- local URLs for core CSS/JS return 200;
- smart component JS requested by the loader returns 200 for demo components;
- HAR contains no CDN/external requests unless explicitly intended;
- HAR contains no old asset version requests after a version migration;
- missing smart packages are shown as unavailable instead of being hidden or faked.
