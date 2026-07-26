# SF5 Component And Smart-Component Catalog

Generated from local source mirrors. Refresh with:

```bash
python3 skills/sf5/scripts/sync_source_repos.py
python3 skills/sf5/scripts/build_component_smart_catalog.py
```

## Summary

- Components: 77
- Components with examples: 34
- Smart-components: 50
- Smart-components with examples: 43

## Use In Conversion

- Prefer entries with `shipped=true` and at least one `playExamples` path.
- Use component entries for presentational replacement of Tailwind blocks.
- Use smart-component entries only when the source behavior requires state, events, data loading, or widget lifecycle.
- Treat `contract.customElements`, `contract.sfCodeValues`, and `contract.attributeExamples` as source-backed hints, not as a complete API spec.

## High-Value Components

- `accordion`: roots `sf-accordion, sf-accordion-content, sf-accordion-title, sf-accordion-wrap, sf-icon`; examples: source/simai/ui-play/examples/components/accordion/default/index.html
- `admin-menu`: roots `sf-admin-menu-bottom, sf-admin-menu-head, sf-admin-menu-head-container, sf-admin-menu-head-logo, sf-admin-menu-item`; examples: source/simai/ui-play/examples/components/admin-menu/default/index.html
- `alerts`: roots `sf-alert, sf-alert-text, sf-alert-wrap, sf-icon, sf-icon-button`; examples: source/simai/ui-play/examples/components/alert/default/index.html
- `avatars`: roots `sf-avatar, sf-avatar-card, sf-avatar-card-content, sf-avatar-card-image, sf-avatar-card-portrait`; examples: source/simai/ui-play/examples/components/avatar/card/index.html, source/simai/ui-play/examples/components/avatar/default/index.html
- `badges`: roots `sf-badge, sf-badge-icon-container, sf-badge-text, sf-badge-text-container, sf-icon`; examples: source/simai/ui-play/examples/components/badges/all/index.html
- `breadcrumbs`: roots `sf-breadcrumbs, sf-breadcrumbs-item, sf-breadcrumbs-item-container, sf-icon`; examples: source/simai/ui-play/examples/components/breadcrumbs/default/index.html
- `buttons`: roots `sf-button, sf-button-text-container, sf-card, sf-icon, sf-text-2`; examples: source/simai/ui-play/examples/components/buttons/all/index.html, source/simai/ui-play/examples/components/buttons/segments/index.html
- `checkbox`: roots `sf-checkbox, sf-checkbox-box, sf-checkbox-container, sf-checkbox-description, sf-checkbox-label`; examples: source/simai/ui-play/examples/components/checkbox/all/index.html
- `close`: roots `sf-close, sf-close-icon, sf-text-1, sf-weight-medium`; examples: source/simai/ui-play/examples/components/close/default/index.html
- `context-menu`: roots `sf-button, sf-button-text-container, sf-context-menu, sf-context-menu-content, sf-context-menu-tooltip`; examples: source/simai/ui-play/examples/components/context-menu/all/index.html
- `datepicker`: roots `sf-button, sf-button-text-container, sf-datepicker, sf-datepicker-container, sf-datepicker-context`; examples: source/simai/ui-play/examples/components/datepicker/default/index.html
- `download-file`: roots `sf-download-file, sf-download-file-container, sf-download-file-file-size, sf-download-file-wrap, sf-icon`; examples: source/simai/ui-play/examples/components/download-file/default/index.html
- `dropdown`: roots `sf-avatar, sf-avatar-label-group, sf-avatar-label-group-container, sf-avatar-label-group-title, sf-checkbox`; examples: source/simai/ui-play/examples/components/dropdown/dropdown/index.html, source/simai/ui-play/examples/components/dropdown/list/index.html
- `featured-icon`: roots `sf-featured-icon, sf-icon`; examples: source/simai/ui-play/examples/components/featured-icon/all/index.html
- `file-preview`: roots `sf-file-preview, sf-file-preview-actions, sf-file-preview-holder, sf-file-preview-main, sf-file-preview-name`; examples: source/simai/ui-play/examples/components/file-preview/default/index.html
- `file-upload`: roots `sf-button, sf-button-text-container, sf-featured-icon, sf-file-upload, sf-file-upload-block`; examples: source/simai/ui-play/examples/components/file-upload/default/index.html, source/simai/ui-play/examples/components/file-upload/interactive/index.html
- `icon-buttons`: roots `sf-card, sf-close, sf-close-icon, sf-icon, sf-icon-button`; examples: source/simai/ui-play/examples/components/icon-buttons/icon-buttons/index.html
- `inputs`: roots `sf-country-code, sf-country-code-field, sf-country-code-flag-icon, sf-country-code-label, sf-country-code-left`; examples: source/simai/ui-play/examples/components/inputs/all/index.html, source/simai/ui-play/examples/components/inputs/country-code/index.html
- `menu`: roots `sf-icon, sf-icon-button, sf-menu, sf-menu-element, sf-menu-element-text`; examples: source/simai/ui-play/examples/components/menu/default/index.html
- `modal`: roots `sf-button, sf-button-text-container, sf-card`; examples: source/simai/ui-play/examples/components/modal/all/index.html
- `pagination`: roots `sf-button, sf-button-text-container, sf-checkbox, sf-checkbox-box, sf-checkbox-container`; examples: source/simai/ui-play/examples/components/pagination/default/index.html, source/simai/ui-play/examples/components/pagination/page-number/index.html
- `placeholder`: roots `sf-button, sf-button-text-container, sf-placeholder, sf-placeholder-left, sf-placeholder-right`; examples: source/simai/ui-play/examples/components/placeholder/default/index.html
- `range-slider`: roots `sf-range-slider, sf-text-2`; examples: source/simai/ui-play/examples/components/range-slider/default/index.html
- `reference-link`: roots `sf-icon, sf-reference-link, sf-reference-link-left, sf-reference-link-text`; examples: source/simai/ui-play/examples/components/reference-link/default/index.html
- `skeleton`: roots `-`; examples: source/simai/ui-play/examples/components/skeleton/default/index.html
- `slider`: roots `sf-icon, sf-icon-button, sf-slider, sf-slider-arrows, sf-slider-button-next`; examples: source/simai/ui-play/examples/components/slider/default/index.html
- `spinner`: roots `sf-loader, sf-loader-container`; examples: source/simai/ui-play/examples/components/spinner/default/index.html
- `step`: roots `sf-icon, sf-step, sf-step-container, sf-steps, sf-steps-container`; examples: source/simai/ui-play/examples/components/step/default/index.html
- `switch`: roots `sf-icon, sf-switch, sf-switch-container, sf-switch-container-wrap, sf-switch-description`; examples: source/simai/ui-play/examples/components/switch/default/index.html
- `tabs`: roots `sf-button, sf-button-text-container, sf-icon, sf-icon-button, sf-tabs`; examples: source/simai/ui-play/examples/components/tabs/default/index.html
- `tags`: roots `sf-avatar, sf-card, sf-checkbox, sf-checkbox-box, sf-close`; examples: source/simai/ui-play/examples/components/tags/all/index.html
- `toast`: roots `sf-button, sf-button-text-container, sf-close, sf-close-icon, sf-icon`; examples: source/simai/ui-play/examples/components/toast/default/index.html
- `toggle`: roots `sf-icon, sf-toggle, sf-toggle-container, sf-toggle-control, sf-toggle-inner`; examples: source/simai/ui-play/examples/components/toggle/default/index.html
- `tooltip`: roots `sf-text-1/2, sf-text-2, sf-tooltip, sf-tooltip-content, sf-tooltip-supporting-text`; examples: source/simai/ui-play/examples/components/tooltip/all/index.html

## High-Value Smart-Components

- `admin-menu`: elements `sf-admin-menu, sf-admin-menu-item`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/admin-menu/default/index.html
- `alert`: elements `sf-alert, sf-button`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/alert/default/index.html
- `avatar`: elements `sf-avatar, sf-button, sf-icon-button, sf-tooltip`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/avatar/element/index.html, source/simai/ui-play/examples/smart-components/avatar/group/index.html
- `avatars`: elements `sf-avatar, sf-icon-button, sf-tooltip`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/avatar/group/index.html
- `badges`: elements `sf-badge`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/badges/element/index.html
- `breadcrumbs`: elements `sf-breadcrumbs`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/breadcrumbs/default/index.html
- `buttons`: elements `sf-button`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/buttons/element/index.html, source/simai/ui-play/examples/smart-components/buttons/events/index.html
- `checkbox`: elements `sf-button, sf-checkbox`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/checkbox/all/index.html
- `context-menu`: elements `sf-button, sf-context-menu`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/context-menu/default/index.html
- `country-code`: elements `sf-country-code`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/inputs/country-code/index.html
- `download-file`: elements `sf-download-file`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/download-file/element/index.html
- `dropdown`: elements `sf-button, sf-dropdown, sf-list-item`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/dropdown/element/index.html
- `editor`: elements `sf-editor`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/editor/default/index.html
- `fab`: elements `sf-fab`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/fab/default/index.html
- `file-upload`: elements `sf-button, sf-file-upload`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/file-upload/element/index.html
- `flags`: elements `sf-flags`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/flags/default/index.html
- `gallery`: elements `sf-button, sf-gallery`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/gallery/default/index.html, source/simai/ui-play/examples/smart-components/gallery/images/index.html
- `icon-buttons`: elements `sf-button, sf-icon-button`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/icon-buttons/element/index.html
- `icons`: elements `sf-icon`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/icons/default/index.html
- `inputs`: elements `sf-button, sf-country-code, sf-input`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/inputs/country-code/index.html, source/simai/ui-play/examples/smart-components/inputs/element/index.html
- `link`: elements `sf-link`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/link/default/index.html
- `list-item`: elements `sf-button, sf-list-item`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/list-item/element/index.html
- `modal`: elements `sf-button, sf-input, sf-modal`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/modal/element/index.html
- `pagination`: elements `sf-pagination`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/pagination/default/index.html
- `progress-bar`: elements `sf-progress-bar`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/progress/progress-bar/index.html
- `progress-scale`: elements `sf-progress-scale`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/progress/progress-scale/index.html
- `radio`: elements `sf-radio`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/radio/all/index.html
- `range-slider`: elements `sf-range-slider`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/range-slider/default/index.html
- `rating`: elements `sf-rating`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/rating/default/index.html
- `reference-link`: elements `sf-reference-link`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/reference-link/default/index.html
- `skeleton`: elements `sf-skeleton`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/skeleton/default/index.html
- `slider`: elements `sf-slider`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/slider/default/index.html
- `spinner`: elements `sf-spinner`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/spinner/default/index.html
- `steps`: elements `sf-steps`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/steps/default/index.html
- `switch`: elements `sf-switch`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/switch/default/index.html
- `table`: elements `sf-table`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/table/default/index.html
- `tabs`: elements `sf-tabs`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/tabs/default/index.html
- `tags`: elements `sf-button, sf-tag`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/tags/element/index.html
- `textarea`: elements `sf-textarea`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/textarea/element/index.html
- `toast`: elements `sf-button, sf-toast`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/toast/default/index.html
- `toggle`: elements `sf-toggle`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/toggle/default/index.html
- `tooltip`: elements `sf-tooltip`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/tooltip/element/index.html
- `tree`: elements `sf-tree, sf-tree-item`; sf-code `-`; examples: source/simai/ui-play/examples/smart-components/tree/default/index.html, source/simai/ui-play/examples/smart-components/tree/item/index.html
