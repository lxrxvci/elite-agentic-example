# EmptyState

Centered placeholder shown when a list or page has no data. Provides a clear next action.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `title` | `string` | — | Short heading, e.g. *“No unbilled time yet”*. |
| `description` | `string` | — | Optional explanatory line. |
| `actionLabel` | `string` | — | Optional CTA label. |
| `onAction` | `() => void` | — | Optional CTA handler. |
| `illustration` | `'none' \| 'document' \| 'clock'` | `'none'` | Optional decorative illustration name. |

## Usage

- Dashboard when there are no recent unbilled entries.
- Time tracker when no entries match filters.
- Invoice list when no invoices exist.
- Quick-entry modal when no clients/projects exist.

## Tokens

| Element | Token / value |
|---|---|
| Background | `semantic.color.background` or parent surface |
| Border | `semantic.color.border` (proposed) when inside a card |
| Title | `semantic.color.text-primary`, `global.font.size-lg`, `weight-bold` |
| Description | `semantic.color.text-secondary`, `global.font.size-base` |
| Padding | `global.spacing.06` |

## Accessibility

- Wrap in a region with `aria-live="polite"` so the empty state is announced when content changes.
- Title uses a heading element (`<h2>` or `<h3>` depending on context).
- Action button receives focus when the empty state is the primary content.
