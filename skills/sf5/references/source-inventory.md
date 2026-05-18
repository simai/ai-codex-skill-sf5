# SF5 Source Inventory

Generated from synced upstream repositories under `source/simai`.

## Source Revisions

- `ui`: `main` @ `ced241ecc312ff683594ead19cee9e410b6541b8`
- `ui-doc`: `main` @ `6ecb05f1fa94dd379d6defd79fa0e0dae0374902`
- `ui-play`: `master` @ `0a393e85f0c6a137ae024f442dd52cc34d5f0508`
- `ui-smart`: `main` @ `36d5f50667c572db513e1fc36d4e23145bb05333`
- `ui-utilities`: `main` @ `7ef2047a65ca5c81604199f997792c9ac0513de4`
- `ui-vscode`: `main` @ `ad9d7815a5aba10e1c548778c1730f0583065ef4`
- `ui-components`: `error` - Cloning into '/Users/rim/Documents/GitHub/ai-codex-skill-sf5/source/simai/ui-components'...
fatal: Remote branch main not found in upstream origin

## Summary

- Shipped components in `ui`: `72`
- Shipped smart-components in `ui-smart`: `34`
- Utility groups in `ui-utilities`: `234`
- Component example groups in `ui-play`: `31`
- Smart example groups in `ui-play`: `31`
- Shipped components without direct component example groups: `41`
- Shipped smart-components without direct smart example groups: `1`

## Practical Reading Order

- For utility/layout work: start with `ui-doc` atlas, then validate class names against `ui-utilities`.
- For presentational components: start with `ui-play/examples/components`, then confirm shipping in `ui/distr/component`.
- For smart-components: start with `ui-play/examples/smart-components`, then confirm runtime presence in `ui-smart/smart`.
- For loader/runtime assumptions: confirm actual boot paths in `ui-play/packages/*/setup-sf.ts` and shipped paths in `ui/distr/core`.

## Component Coverage

- `accordion`: `components/accordion/default`
- `alerts`: `alert`
- `avatars`: `avatar`
- `avatars-group`: `avatar`
- `badges`: `components/badges/all`
- `buttons`: `components/buttons/all, components/buttons/tightness`
- `checkbox`: `components/checkbox/all`
- `close`: `components/close/default`
- `context-menu`: `components/context-menu/all`
- `download-file`: `components/download-file/default`
- `dropdown`: `components/dropdown/dropdown, components/dropdown/list, components/dropdown/list-item`
- `featured-icon`: `components/featured-icon/all`
- `file-upload`: `components/file-upload/default, components/file-upload/interactive`
- `icon-buttons`: `components/icon-buttons/icon-buttons`
- `inputs`: `components/inputs/textarea`
- `menu`: `components/menu/default`
- `modal`: `components/modal/all`
- `pagination`: `components/pagination/default, components/pagination/page-number`
- `placeholder`: `components/placeholder/default`
- `progress`: `components/progress/default, components/progress/progress-scale`
- `range-slider`: `components/range-slider/default`
- `reference-link`: `components/reference-link/default`
- `skeleton`: `components/skeleton/default`
- `slider`: `components/slider/default`
- `spinner`: `components/spinner/default`
- `step`: `components/step/default`
- `switch`: `components/switch/default`
- `tags`: `components/tags/all`
- `toast`: `components/toast/default`
- `toggle`: `components/toggle/default`
- `tooltip`: `components/tooltip/all`

Direct component-example gaps:

- `ajax`
- `ajaxload`
- `breadcrumbs`
- `carousel`
- `clipboard`
- `contentDivider`
- `country-code`
- `doc`
- `dot`
- `emoji`
- `fab`
- `fancybox`
- `fileUpload`
- `hideShow`
- `highlight`
- `icon`
- `icons`
- `jquery`
- `lazy-load`
- `monaco`
- `overbox`
- `overcard`
- `progress-bar`
- `progress-scale`
- `progressbar`
- `quantity`
- `radio`
- `scrollbar`
- `sf-system`
- `share`
- `special`
- `swiper`
- `tab`
- `tabs`
- `textarea`
- `theme`
- `theme-builder`
- `verification`
- `viewbox`
- `waves`
- `... +1 more`

## Smart-Component Coverage

- `alert`: `smart-components/alert/default`
- `avatar`: `smart-components/avatar/element, smart-components/avatar/group`
- `avatars`: `avatar/group`
- `badges`: `smart-components/badges/element`
- `buttons`: `smart-components/buttons/element, smart-components/buttons/events`
- `checkbox`: `smart-components/checkbox/all`
- `context-menu`: `smart-components/context-menu/default`
- `country-code`: `inputs/country-code`
- `download-file`: `smart-components/download-file/element`
- `dropdown`: `smart-components/dropdown/element`
- `file-upload`: `smart-components/file-upload/element`
- `gallery`: `smart-components/gallery/default, smart-components/gallery/images`
- `icon-buttons`: `smart-components/icon-buttons/element`
- `icons`: `smart-components/icons/default`
- `inputs`: `smart-components/inputs/country-code, smart-components/inputs/element`
- `list-item`: `smart-components/list-item/element`
- `modal`: `smart-components/modal/element`
- `pagination`: `smart-components/pagination/default`
- `progress-bar`: `progress/progress-bar`
- `progress-scale`: `progress/progress-scale`
- `radio`: `smart-components/radio/all`
- `range-slider`: `smart-components/range-slider/default`
- `reference-link`: `smart-components/reference-link/default`
- `skeleton`: `smart-components/skeleton/default`
- `slider`: `smart-components/slider/default`
- `spinner`: `smart-components/spinner/default`
- `steps`: `smart-components/steps/default`
- `switch`: `smart-components/switch/default`
- `tags`: `smart-components/tags/element`
- `textarea`: `smart-components/textarea/element`
- `toast`: `smart-components/toast/default`
- `toggle`: `smart-components/toggle/default`
- `tooltip`: `smart-components/tooltip/element`

Direct smart-example gaps:

- `close`

## Utility Example Groups

- `animation`
- `backdrop-filter`
- `background`
- `border`
- `divider`
- `filters`
- `flex`
- `forms`
- `grid`
- `grid-and-flexbox-utilities`
- `indents`
- `interactivity`
- `layout`
- `layout-break`
- `links`
- `mask`
- `objects`
- `outline`
- `overscroll`
- `print`
- `shadows`
- `sizes`
- `stripes`
- `svg`
- `tables`
- `text-formatting`
- `transform`
- `typography`
