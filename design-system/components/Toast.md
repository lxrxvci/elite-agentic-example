# Toast

Non-blocking feedback message. Used after save actions, duplicate warnings, and errors.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `'success' \| 'error' \| 'info'` | `'info'` | Visual treatment and ARIA role. |
| `title` | `string` | — | Bold headline. |
| `message` | `string` | — | Supporting text. |
| `actionLabel` | `string` | — | Optional action button label. |
| `onAction` | `() => void` | — | Optional action callback. |
| `onDismiss` | `() => void` | — | Dismiss callback. |
| `duration` | `number` | `5000` | Auto-dismiss timeout in ms; `0` disables auto-dismiss. |

## Usage

- **Success:** *“20 minutes logged for Acme Corp — Website Redesign”*.
- **Info:** duplicate-entry prompt with **Save anyway** action.
- **Error:** server errors or validation failures that cannot be tied to a field.

## Tokens

| Element | Token / value |
|---|---|
| Background | `semantic.color.background` |
| Border | `semantic.color.border` (proposed) |
| Shadow | `component.card.shadow` (proposed) |
| Radius | `global.radius.md` |
| Success icon | `semantic.color.success` (proposed) |
| Error icon | `semantic.color.danger` |
| Info icon | `semantic.color.interactive` |
| Title | `semantic.color.text-primary`, `weight-medium` |
| Message | `semantic.color.text-secondary` |

## Accessibility

- Use `role="status"` for success/info; `role="alert"` for errors.
- `aria-live="polite"` so announcements do not interrupt.
- Do not move focus into the toast unless it contains an action the user must take.
- Dismiss button has accessible label *“Dismiss notification”*.
- Pause auto-dismiss while the toast is hovered or focused.
