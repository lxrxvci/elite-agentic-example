# Developer Handoff — Bet 1: Capture More Billable Hours

*Bridge document for Frontend Engineering. Assumes `/design-system/tokens.json`, `openapi.yaml`, `USER_FLOWS.md`, `WIREFRAMES.md`, and `ACCESSIBILITY_CHECKLIST.md` have been read.*

---

## 1. Component inventory

Map of every screen/global feature to the design-system components that should be used or created.

| Screen / feature | Components used | New? | Notes |
|---|---|---|---|
| **Global nav** | `Logo`, `NavLink`, `Button`, `AvatarMenu`, `Tooltip` | Mixed | `+ Log time` uses `Button` primary; shortcut hint in tooltip + `aria-description`. |
| **Quick-entry modal** | `QuickEntryModal` (NEW), `Select`, `Textarea`, `Input`, `Button`, `Toast` | **Yes** | Focus trap, MRU defaults, validation, duplicate recovery, empty state. |
| **Live timer** | `LiveTimerPill` (NEW), `Button` | **Yes** | Client-only persistence; 15-min rounding; recovery banner. |
| **Dashboard** | `UnbilledSummaryCard` (NEW), `TimeEntryRow` (NEW), `InvoiceCard` (NEW), `StatusBadge` (NEW), `EmptyState` (NEW), `Button`, `Skeleton` | **Yes** | Tables/lists assembled in page widgets; bulk action bar is a local widget. |
| **Time tracker** | `TimeEntryRow`, `StatusBadge`, `EmptyState`, `Button`, `FilterBar` (local), `Pagination` (local) | Reuses new atoms | “Select all unbilled” selects only rows with `status=unbilled`. |
| **Invoice list** | `InvoiceCard`, `StatusBadge`, `EmptyState`, `Button`, `FilterBar` (local), `Pagination` (local) | Reuses new atoms | Draft rows expose **Send** action. |
| **Invoice detail** | `InvoiceCard` (header), `InvoiceLineItemTable` (NEW), `RecordPaymentDialog` (NEW), `StatusBadge`, `Button` | **Yes** | Primary action adapts to invoice status. |
| **Invoice create** | `SelectableTimeEntryGroup` (NEW), `TimeEntryRow`, `Button`, `Input`, `Textarea` | **Yes** | Grouped selection; single-client validation. |

### New components to spec

All new components are specified in `/design-system/components/`:

- `Button.md`
- `StatusBadge.md`
- `EmptyState.md`
- `Toast.md`
- `QuickEntryModal.md`
- `LiveTimerPill.md`
- `TimeEntryRow.md`
- `InvoiceCard.md`
- `UnbilledSummaryCard.md`
- `RecordPaymentDialog.md`
- `InvoiceLineItemTable.md`
- `SelectableTimeEntryGroup.md`

---

## 2. Token usage table

### Existing tokens (from `tokens.json`)

| Token | Value | Usage |
|---|---|---|
| `global.color.gray-900` | `#111827` | Primary text, headings, table body text. |
| `global.color.gray-500` | `#6b7280` | Secondary text, placeholders, hints, disabled text. |
| `global.color.gray-100` | `#f3f4f6` | Surface backgrounds, table row hover, stripes. |
| `global.color.white` | `#ffffff` | Page background, modal background, primary button text. |
| `global.color.blue-600` | `#2563eb` | Interactive accent, focus rings, links, unbilled badge. |
| `global.color.red-600` | `#dc2626` | Danger, errors, overdue status, discard actions. |
| `global.font.sans` | `Inter, system-ui, sans-serif` | All UI text. |
| `global.font.size-sm` | `0.875rem` | Labels, captions, table headers, badges. |
| `global.font.size-base` | `1rem` | Body, inputs, buttons. |
| `global.font.size-lg` | `1.125rem` | Card headings, invoice totals. |
| `global.font.size-xl` | `1.25rem` | Dashboard metric. |
| `global.font.size-2xl` | `1.5rem` | Dashboard unbilled total. |
| `global.font.weight-medium` | `500` | Labels, nav links, button text. |
| `global.font.weight-bold` | `700` | Headings, totals, metric. |
| `global.spacing.02` | `0.5rem` | Button padding-y, small gaps. |
| `global.spacing.03` | `0.75rem` | Badge padding, pill inner spacing. |
| `global.spacing.04` | `1rem` | Card padding, button padding-x. |
| `global.spacing.06` | `1.5rem` | Section gaps, modal padding. |
| `global.radius.md` | `0.375rem` | Buttons, inputs, badges, table cells. |
| `global.radius.lg` | `0.5rem` | Cards, modal, pill, dialog. |
| `semantic.color.text-primary` | `{global.color.gray-900}` | Body text. |
| `semantic.color.text-secondary` | `{global.color.gray-500}` | Hints, meta text. |
| `semantic.color.background` | `{global.color.white}` | Page, modal. |
| `semantic.color.surface` | `{global.color.gray-100}` | Cards, hover, bulk bar. |
| `semantic.color.interactive` | `{global.color.blue-600}` | Primary actions, focus rings. |
| `semantic.color.danger` | `{global.color.red-600}` | Errors, overdue. |
| `component.button-primary.background` | `{semantic.color.interactive}` | Primary buttons. |
| `component.button-primary.text` | `{global.color.white}` | Primary button labels. |
| `component.button-primary.radius` | `{global.radius.md}` | Primary buttons. |
| `component.button-primary.padding-x` | `{global.spacing.04}` | Primary buttons. |
| `component.button-primary.padding-y` | `{global.spacing.02}` | Primary buttons. |

### Proposed tokens (add to `tokens.json`)

| Token | Value | Usage |
|---|---|---|
| `semantic.color.border` | `#e5e7eb` | Card borders, table borders, input borders, nav divider. |
| `semantic.color.success` | `#16a34a` | Paid status, success toasts. |
| `semantic.color.warning` | `#d97706` | Sent status, upcoming due warnings. |
| `component.input.border` | `{semantic.color.border}` | Input borders. |
| `component.input.radius` | `{global.radius.md}` | Input corners. |
| `component.input.padding` | `{global.spacing.03}` | Input inner spacing. |
| `component.modal.overlay` | `rgba(0,0,0,0.5)` | Modal / dialog backdrop. |
| `component.card.shadow` | `0 4px 6px -1px rgba(0,0,0,0.1)` | Cards, floating pill. |
| `component.focus-ring.width` | `2px` | Focus indicator thickness. |
| `component.focus-ring.color` | `{semantic.color.interactive}` | Focus indicator color. |

---

## 3. Interaction specs

### Animations & transitions

| Element | Trigger | Effect | Duration | Easing |
|---|---|---|---|---|
| Modal | open/close | opacity + slight scale (`0.98 → 1`) | 150ms | ease-out / ease-in |
| Toast | appear/dismiss | slide down + fade | 200ms | ease-out |
| Live timer pill | start timer | slide up from bottom-right | 200ms | ease-out |
| Button | hover/active | background-color / translate-y | 100ms | ease |
| Table row | hover | background-color | 100ms | ease |
| Skeleton | loading | shimmer translate-x | 1.5s | linear infinite |
| Focus ring | focus | instant outline | 0ms | — |

- Respect `prefers-reduced-motion`: disable translate/scale; keep opacity-only or instant transitions.

### Responsive behavior

| Breakpoint | Layout changes |
|---|---|
| `≥1024px` | Full multi-column layouts; modal centered; timer pill floating. |
| `768–1023px` | Tables keep structure; optional columns (Issue date, Project) collapse into expandable rows. Filters wrap. |
| `<768px` | Tables become stacked cards (`InvoiceCard`, `TimeEntryRow` stacked layout); modal becomes full-screen sheet; timer pill becomes full-width bottom bar. |

### Keyboard & shortcuts

- `Cmd/Ctrl + Shift + T`: open quick-entry modal from any page. Press again to close while preserving draft for 60s.
- `Esc`: close modal / dialog; returns focus to trigger.
- `Tab`: moves focus inside modal/dialog; trapped until closed.
- `Enter`: submits form when focused on a submit button or in a single-line field.
- `Space`: toggles checkboxes.
- Dashboard time table: `Tab` moves select-all → row checkbox → row link → bulk actions.

### State persistence

- **MRU client/project:** stored in `localStorage` under `time-capture.mru`; updated on every successful save.
- **Live timer start timestamp:** stored in `sessionStorage` (`time-capture.timerStart`) so a refresh can recover elapsed time.
- **Quick-entry draft:** partial input preserved for 60s after modal close in `sessionStorage` (`time-capture.draft`).

---

## 4. API endpoint mapping

| UI element | OpenAPI operation | Method / path | Request / query | Response usage |
|---|---|---|---|---|
| User name, tenant, default rate | `getCurrentUser` | `GET /me` | — | `name`, `tenant.default_hourly_rate`, `tenant.default_currency` |
| Client dropdown | `listClients` | `GET /clients` | `limit`, `offset` | `items[].id`, `items[].name`, `items[].default_hourly_rate` |
| Project dropdown (filtered by client) | `listProjects` | `GET /projects` | `client_id`, `limit`, `offset` | `items[].id`, `items[].name`, `items[].rounding_minutes` |
| Save manual time entry | `createTimeEntry` | `POST /time-entries` | `TimeEntryCreate` body | New entry → toast + dashboard update |
| Update time entry from detail panel | `updateTimeEntry` | `PATCH /time-entries/{timeEntryId}` | `TimeEntryUpdate` body | Updated entry → list refresh |
| Dashboard recent unbilled | `listTimeEntries` | `GET /time-entries` | `status=unbilled`, `limit` | Rows for dashboard table |
| Time tracker list | `listTimeEntries` | `GET /time-entries` | `client_id`, `project_id`, `status`, `from`, `to`, `limit`, `offset` | Paginated table data |
| Invoice list | `listInvoices` | `GET /invoices` | `status`, `client_id`, `limit`, `offset` | Rows for invoice list |
| Invoice detail | `getInvoice` | `GET /invoices/{invoiceId}` | — | Header, line items, totals, status |
| Create draft invoice | `createInvoice` | `POST /invoices` | `InvoiceCreate` body | New invoice + selected entries marked `billed` |
| Mark invoice paid | `markInvoicePaid` | `POST /invoices/{invoiceId}/mark-paid` | `InvoiceMarkPaid` body | Status → `paid`; refresh dashboard |
| **Send invoice** (Draft → Sent) | *(not in current OpenAPI)* | `PATCH /invoices/{invoiceId}` or `POST /invoices/{invoiceId}/send` | `{ status: "sent" }` | **To be added by Backend/Tech Lead** |
| **Download PDF** | *(not in current OpenAPI)* | `GET /invoices/{invoiceId}/pdf` | — | **To be added by Backend/Tech Lead** |
| **Duplicate invoice** | *(not in current OpenAPI)* | `POST /invoices/{invoiceId}/duplicate` | — | **To be added by Backend/Tech Lead** |

### Error handling notes

- `400 ValidationError` → map `pointer` to field names; display inline errors.
- `409 Conflict` on `POST /time-entries` → show duplicate toast with **Save anyway**.
- `409 Conflict` on `POST /invoices` → one or more selected entries already billed; refresh list.
- `422 UnprocessableEntity` on invoice create → mixed-client entries; show multi-client inline error.

---

## 5. Accessibility annotations (beyond the checklist)

### Global

- **Focus management:** every interactive element has a visible 2px focus ring using `semantic.color.interactive`. Focus order follows the keyboard reference in `ACCESSIBILITY_CHECKLIST.md`.
- **Color independence:** status is never color-only. Badges include text + optional icon; overdue rows add a danger left-border.
- **Reduced motion:** all motion respects `prefers-reduced-motion`.

### Quick-entry modal

- Use the native `<dialog>` element or `role="dialog"` with `aria-modal="true"`.
- `aria-labelledby="modal-title"`; helper text linked via `aria-describedby`.
- Each `<select>` / `<textarea>` / `<input>` has a persistent visible `<label>` (not placeholder-only).
- Inline error messages are linked to inputs with `aria-describedby` and announced via an `aria-live="polite"` region.
- When the modal opens, focus moves to the Description field. On close, focus returns to the element that triggered it.

### Live timer pill

- Elapsed time is in an `aria-live="polite"` region; updates announced at 15-minute intervals, not every second.
- Start/Stop/Discard buttons update their accessible labels to reflect current state (e.g. *“Stop timer at 1 hour 15 minutes”*).
- Pill maintains ≥4.5:1 contrast against the page background.

### Tables (Dashboard, Time tracker, Invoice list)

- Use semantic `<table>`, `<thead>`, `<tbody>`, `<th scope="col">`.
- Row checkboxes use `aria-label` that includes client, project, description, and duration.
- Bulk action bar is a live region (`aria-live="polite"`) so selection changes are announced.
- Pagination controls announce current/total pages via `aria-label`.

### Invoice detail

- Invoice number is the `<h1>`; status is a visible subheading, not only a badge.
- Line-item table uses `<th scope="col">`; monetary columns are right-aligned.
- Primary action changes by status; the button text update is announced by `aria-live="polite"`.
- **Record payment** opens a `<dialog>` that traps focus and returns focus to the trigger on close.

### Invoice create

- Group headers are exposed as headings; group checkbox `aria-label` includes client/project name and entry count.
- Multi-client error is announced via `aria-live="assertive"` when it appears.
- Summary totals use an `<output>` or live region so amount changes are announced as entries are selected.
