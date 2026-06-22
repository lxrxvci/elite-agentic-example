# StatusBadge

Small, non-interactive label used for time-entry and invoice statuses. Color is secondary — the text label is always visible.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `status` | `'unbilled' \| 'billed' \| 'draft' \| 'sent' \| 'paid' \| 'overdue' \| 'cancelled'` | — | Status value. |
| `size` | `'sm' \| 'md'` | `'md'` | Badge size. |
| `icon` | `'none' \| 'leading'` | `'leading'` | Whether to show a status dot/icon. |

## Usage

- Time-entry rows: `unbilled`, `billed`.
- Invoice rows/detail: `draft`, `sent`, `paid`, `overdue`, `cancelled`.

## Tokens

| Status | Background | Text / icon |
|---|---|---|
| `unbilled` | `rgba(37, 99, 235, 0.12)` | `global.color.blue-600` |
| `billed` | `semantic.color.surface` | `semantic.color.text-secondary` |
| `draft` | `semantic.color.surface` | `semantic.color.text-secondary` |
| `sent` | `rgba(217, 119, 6, 0.12)` | `semantic.color.warning` (proposed `#d97706`) |
| `paid` | `rgba(22, 163, 74, 0.12)` | `semantic.color.success` (proposed `#16a34a`) |
| `overdue` | `rgba(220, 38, 38, 0.12)` | `semantic.color.danger` |
| `cancelled` | `semantic.color.surface` | `semantic.color.text-secondary` |

- Radius: `global.radius.md`.
- Padding: `global.spacing.02` `global.spacing.03`.
- Font: `global.font.size-sm` / `weight-medium`.

## Accessibility

- Render as `<span>`; not focusable.
- Always include visible text; do not rely on color alone.
- Leading icon is decorative (`aria-hidden="true"`).
