# Button

Action trigger. Primary variant maps directly to the existing `component.button-primary` token.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `'primary' \| 'secondary' \| 'danger' \| 'ghost'` | `'primary'` | Visual style. |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Padding and font size. |
| `disabled` | `boolean` | `false` | Disables pointer and keyboard interaction. |
| `loading` | `boolean` | `false` | Shows a spinner and sets `aria-busy`. |
| `children` | `ReactNode` | — | Button label. |
| `onClick` | `() => void` | — | Click handler. |
| `type` | `'button' \| 'submit' \| 'reset'` | `'button'` | Native button type. |

## Usage

- **Primary:** `+ Log time`, Save, Send invoice, Create draft.
- **Secondary:** Cancel, Close.
- **Danger:** Discard timer, Cancel invoice.
- **Ghost:** row actions such as Edit, Duplicate, Send reminder.

## Tokens

| Element | Token / value |
|---|---|
| Primary bg | `component.button-primary.background` → `semantic.color.interactive` |
| Primary text | `component.button-primary.text` → `global.color.white` |
| Primary radius | `component.button-primary.radius` → `global.radius.md` |
| Primary padding | `component.button-primary.padding-x` / `padding-y` |
| Secondary bg | `semantic.color.background` |
| Secondary border | `semantic.color.border` (proposed `#e5e7eb`) |
| Secondary text | `semantic.color.text-primary` |
| Danger bg | `semantic.color.danger` |
| Danger text | `global.color.white` |
| Ghost text | `semantic.color.interactive` |
| Hover darken | `-10%` background luminosity |
| Active darken | `-15%` background luminosity |
| Focus ring | `component.focus-ring.width` `component.focus-ring.color` |
| Disabled | `opacity: 0.5` |

## Accessibility

- Render as a native `<button>`.
- Expose `disabled` attribute when disabled; do not move focus.
- When `loading` is true, set `aria-busy="true"` and keep the visible label (spinner is decorative).
- Visible focus ring on `:focus-visible`.
