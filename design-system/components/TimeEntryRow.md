# TimeEntryRow

Row component for a single time entry. Used inside tables on the Dashboard and Time tracker, and inside selectable groups on the Invoice create screen.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `id` | `string` | — | Entry ID. |
| `date` | `string` | — | Display date. |
| `clientName` | `string` | — | Client name. |
| `projectName` | `string` | — | Project name. |
| `description` | `string` | — | Entry description. |
| `durationText` | `string` | — | Raw duration label, e.g. `0h 30m`. |
| `roundedDurationText` | `string` | — | Rounded duration label. |
| `status` | `'unbilled' \| 'billed'` | — | Billing status. |
| `isSelected` | `boolean` | `false` | Checkbox state. |
| `selectable` | `boolean` | `true` | Whether the checkbox is shown. |
| `onSelect` | `(id: string, selected: boolean) => void` | — | Checkbox change handler. |
| `onClick` | `(id: string) => void` | — | Row click handler (opens detail). |

## Usage

- Dashboard “Recent unbilled time” table.
- Time tracker paginated table.
- Invoice create selectable groups.

## Tokens

| Element | Token / value |
|---|---|
| Row bg default | transparent |
| Row bg hover | `semantic.color.surface` |
| Selected accent | 3px left border `semantic.color.interactive` |
| Primary text | `semantic.color.text-primary` |
| Meta text | `semantic.color.text-secondary` |
| Border | `semantic.color.border` (proposed) |
| Status badge | `StatusBadge` |

## Behavior

- Clicking the row (outside the checkbox) opens the entry detail / edit panel.
- Checkbox toggles selection for bulk actions.
- Status badge updates when the entry becomes `billed`.

## Accessibility

- Inside a `<table>`, render as `<tr>`.
- Checkbox `aria-label` includes row context: *“Select entry, {client}, {project}, {description}, {duration}”*.
- Status badge uses visible text label.
- Row has `cursor: pointer` but is not itself focusable; keyboard users tab to the checkbox and the description link.
