# SelectableTimeEntryGroup

Expandable group of time entries used on the invoice create screen. Entries are grouped by client and project.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `clientName` | `string` | — | Client name for the group header. |
| `projectName` | `string` | — | Project name for the group header. |
| `entries` | `TimeEntryRow[]` | `[]` | Entries in the group. |
| `selectedIds` | `string[]` | `[]` | Currently selected entry IDs. |
| `onToggleEntry` | `(id: string) => void` | — | Toggle a single entry. |
| `onToggleGroup` | `() => void` | — | Toggle all entries in the group. |
| `isExpanded` | `boolean` | `true` | Whether rows are visible. |

## Usage

- Invoice create screen.
- First group expanded by default; others collapsed if the list is long.

## Tokens

| Element | Token / value |
|---|---|
| Group header bg | `semantic.color.surface` |
| Group header border | `semantic.color.border` (proposed) |
| Group radius | `global.radius.md` |
| Group padding | `global.spacing.04` |
| Row hover | `semantic.color.surface` |
| Row border | `semantic.color.border` (proposed) |

## Behavior

- Group checkbox reflects partial selection (indeterminate state when some rows selected).
- Selecting entries across multiple clients triggers a validation message and a **Create invoices for each client** action.
- Group header shows total entry count and summed rounded duration.

## Accessibility

- Group header is a heading; use `<fieldset>` / `<legend>` semantics or `role="group"` with `aria-label`.
- Group checkbox `aria-label`: *“Select all {n} entries for {client} — {project}”*.
- Individual row checkboxes inherit labels from `TimeEntryRow`.
- Selection summary announced via `aria-live="polite"`.
