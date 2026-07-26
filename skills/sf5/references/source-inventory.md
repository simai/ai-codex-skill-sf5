# SF5 Source Inventory

Generated from synced upstream repositories under `source/simai`.

## Source Revisions

- `ui`: `main` @ `ff47bd694b6c0ed61b7ad4824f986d99b150cbea`
- `ui-loader`: `main` @ `3ca31c6c2c50ca099b51ce3c25251c71d4860317`
- `ui-doc`: `main` @ `85148eb2c0ba0b21d497ecb912085337a37a7d88`
- `ui-play`: `master` @ `bdd253aaa3418bee7f51b4b69d8e5c08af49ee58`
- `ui-smart`: `main` @ `ab896dc7cd33f151377e3992ffb286769beee7f7`
- `ui-vscode`: `main` @ `a8fd4a8dcd75ce53d2af0c07186fb0ef3b907058`
- `ui-components`: `error` - Cloning into '/Users/rim/Documents/GitHub/ai-codex-skill-sf5/source/simai/ui-components'...
fatal: Remote branch main not found in upstream origin

## Summary

- Shipped components in `ui`: `77`
- Shipped smart-components in `ui-smart`: `50`
- Shipped utility groups in `ui`: `225`
- Utility source groups in `ui-loader`: `226`
- Component example groups in `ui-play`: `37`
- Smart example groups in `ui-play`: `42`
- Shipped components without direct component example groups: `43`
- Shipped smart-components without direct smart example groups: `7`

## Practical Reading Order

- For utility/layout work: start with the `ui-doc` atlas, validate shipped groups in `ui`, then inspect rule and state semantics in `ui-loader`.
- For presentational components: start with `ui-play/examples/components`, then confirm shipping in `ui/distr/component`.
- For smart-components: start with `ui-play/examples/smart-components`, then confirm runtime presence in `ui-smart/smart`.
- For loader/runtime assumptions: confirm actual boot paths in `ui-play/packages/*/setup-sf.ts` and shipped paths in `ui/distr/core`.

## Component Coverage

- `accordion`: `components/accordion/default`
- `admin-menu`: `components/admin-menu/default`
- `alerts`: `alert`
- `avatars`: `avatar`
- `badges`: `components/badges/all`
- `breadcrumbs`: `components/breadcrumbs/default`
- `buttons`: `components/buttons/all, components/buttons/segments, components/buttons/tightness`
- `checkbox`: `components/checkbox/all`
- `close`: `components/close/default`
- `context-menu`: `components/context-menu/all`
- `datepicker`: `components/datepicker/default`
- `download-file`: `components/download-file/default`
- `dropdown`: `components/dropdown/dropdown, components/dropdown/list, components/dropdown/list-item`
- `featured-icon`: `components/featured-icon/all`
- `file-preview`: `components/file-preview/default`
- `file-upload`: `components/file-upload/default, components/file-upload/interactive`
- `icon-buttons`: `components/icon-buttons/icon-buttons`
- `inputs`: `components/inputs/all, components/inputs/country-code, components/inputs/quantity, components/inputs/textarea, components/inputs/verification`
- `menu`: `components/menu/default`
- `modal`: `components/modal/all`
- `pagination`: `components/pagination/default, components/pagination/page-number`
- `placeholder`: `components/placeholder/default`
- `range-slider`: `components/range-slider/default`
- `reference-link`: `components/reference-link/default`
- `skeleton`: `components/skeleton/default`
- `slider`: `components/slider/default`
- `spinner`: `components/spinner/default`
- `step`: `components/step/default`
- `switch`: `components/switch/default`
- `tabs`: `components/tabs/default`
- `tags`: `components/tags/all`
- `toast`: `components/toast/default`
- `toggle`: `components/toggle/default`
- `tooltip`: `components/tooltip/all`

Direct component-example gaps:

- `ajax`
- `ajaxload`
- `carousel`
- `clipboard`
- `contentDivider`
- `country-code`
- `doc`
- `dot`
- `emoji`
- `fab`
- `fancybox`
- `flags`
- `hideShow`
- `highlight`
- `icon`
- `icons`
- `jquery`
- `lazy-load`
- `link`
- `list`
- `monaco`
- `overbox`
- `overcard`
- `progress-bar`
- `progress-scale`
- `quantity`
- `radio`
- `rating`
- `scrollbar`
- `sf-system`
- `share`
- `special`
- `swiper`
- `tab`
- `textarea`
- `theme`
- `theme-builder`
- `tree`
- `tree-item`
- `verification`
- `... +3 more`

## Smart-Component Coverage

- `admin-menu`: `smart-components/admin-menu/default`
- `alert`: `smart-components/alert/default`
- `avatar`: `smart-components/avatar/element, smart-components/avatar/group`
- `avatars`: `avatar/group`
- `badges`: `smart-components/badges/element`
- `breadcrumbs`: `smart-components/breadcrumbs/default`
- `buttons`: `smart-components/buttons/element, smart-components/buttons/events`
- `checkbox`: `smart-components/checkbox/all`
- `context-menu`: `smart-components/context-menu/default`
- `country-code`: `inputs/country-code`
- `download-file`: `smart-components/download-file/element`
- `dropdown`: `smart-components/dropdown/element`
- `editor`: `smart-components/editor/default`
- `fab`: `smart-components/fab/default`
- `file-upload`: `smart-components/file-upload/element`
- `flags`: `smart-components/flags/default`
- `gallery`: `smart-components/gallery/default, smart-components/gallery/images`
- `icon-buttons`: `smart-components/icon-buttons/element`
- `icons`: `smart-components/icons/default`
- `inputs`: `smart-components/inputs/country-code, smart-components/inputs/element, smart-components/inputs/password`
- `link`: `smart-components/link/default`
- `list-item`: `smart-components/list-item/element`
- `modal`: `smart-components/modal/element`
- `pagination`: `smart-components/pagination/default`
- `progress-bar`: `progress/progress-bar`
- `progress-scale`: `progress/progress-scale`
- `radio`: `smart-components/radio/all`
- `range-slider`: `smart-components/range-slider/default`
- `rating`: `smart-components/rating/default`
- `reference-link`: `smart-components/reference-link/default`
- `skeleton`: `smart-components/skeleton/default`
- `slider`: `smart-components/slider/default`
- `spinner`: `smart-components/spinner/default`
- `steps`: `smart-components/steps/default`
- `switch`: `smart-components/switch/default`
- `table`: `smart-components/table/default`
- `tabs`: `smart-components/tabs/default`
- `tags`: `smart-components/tags/element`
- `textarea`: `smart-components/textarea/element`
- `toast`: `smart-components/toast/default`
- `toggle`: `smart-components/toggle/default`
- `tooltip`: `smart-components/tooltip/element`
- `tree`: `smart-components/tree/default, smart-components/tree/item`

Direct smart-example gaps:

- `close`
- `datepicker`
- `drawer`
- `file-preview`
- `form`
- `list`
- `tree-item`

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
- `utilities`
