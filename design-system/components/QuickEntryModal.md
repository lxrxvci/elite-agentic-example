# QuickEntryModal

Global modal for capturing a time entry in under 10 seconds. Reached from the nav button or `Cmd/Ctrl + Shift + T`.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `isOpen` | `boolean` | — | Controls visibility. |
| `onClose` | `() => void` | — | Called on close, escape, or overlay click. |
| `onSave` | `(entry: TimeEntryCreate) => void` | — | Called when the form is valid and submitted. |
| `clients` | `Client[]` | `[]` | Options for the Client select. |
| `projects` | `Project[]` | `[]` | Options for the Project select; filtered by selected client. |
| `defaultClientId` | `string` | — | Initial client selection (MRU). |
| `defaultProjectId` | `string` | — | Initial project selection (MRU). |
| `onAddClient` | `() => void` | — | CTA for the empty state when no clients exist. |

## Usage

- Rendered in the root layout so it can be opened from any page.
- Two internal tabs: **Manual entry** and **Timer**.
- On timer stop, switches to Manual tab with Duration pre-filled and focus moved to Description.

## Tokens

| Element | Token / value |
|---|---|
| Overlay | `component.modal.overlay` (proposed `rgba(0,0,0,0.5)`) |
| Container bg | `semantic.color.background` |
| Container radius | `global.radius.lg` |
| Container padding | `global.spacing.06` |
| Container shadow | `0 20px 25px -5px rgba(0,0,0,0.1)` |
| Input border | `component.input.border` (proposed) |
| Input radius | `component.input.radius` |
| Input padding | `component.input.padding` |
| Error text | `semantic.color.danger` |
| Character counter | `semantic.color.text-secondary`, `size-sm` |

## Behavior

- **Focus trap:** `Tab` cycles inside the modal; `Esc` closes.
- **Initial focus:** Description field on open.
- **MRU defaults:** select the most recently used client/project; fallback to first active pair.
- **Dependent selects:** changing Client filters available Projects.
- **Validation:** description required; duration must be parseable and non-negative.
- **Duplicate handling:** on `409 Conflict`, render a `Toast` with **Save anyway**.
- **Draft restore:** preserve partial input in `sessionStorage` for 60s after close.
- **Empty state:** when `clients.length === 0`, show compact EmptyState with **Add your first client** CTA.

## Accessibility

- Use native `<dialog>` or `role="dialog"` with `aria-modal="true"`.
- `aria-labelledby` references the modal title.
- Each field has a visible `<label>`; helper text linked via `aria-describedby`.
- Inline errors linked to inputs via `aria-describedby`; announced via `aria-live="polite"`.
- Return focus to the trigger element on close.
