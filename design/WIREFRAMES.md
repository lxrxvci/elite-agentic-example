# Wireframes — Bet 1: Capture More Billable Hours

*Text-based wireframes for the four key screens, plus the global quick-entry widget and live-timer indicator. Uses the existing design-system tokens (`tokens.json`); no new components are introduced.*

---

## Global elements

### Top navigation

```text
[Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time]   [Avatar ▼]
                              ^ shortcut hint: Ctrl/Cmd+Shift+T
```

- `+ Log time` is a primary button using `component.button-primary` tokens.
- Keyboard shortcut hint appears on hover/focus as `aria-description` and tooltip.

### Live timer floating indicator (appears bottom-right when running)

```text
+--------------------------------+
| ⏱  1h 15m    [Stop]  [Discard] |
+--------------------------------+
```

- Always stays on top (`z-index` token value TBD by UI Technologist).
- `aria-live="polite"` announces elapsed time every 15 minutes, not every second.

### Quick-entry modal (global)

```text
+--------------------------------------------------+
| Log time                                   [×]    |
+--------------------------------------------------+
| Client:  [Acme Corp              ▼]              |
| Project: [Website Redesign       ▼]              |
|                                                  |
| Description                                      |
| [Revised homepage hero copy                      ]|
| 0/2000                                           |
|                                                  |
| Duration: [20m                 ]  or  [Timer]    |
|                                                  |
| [Cancel]              [Save: 20 min → 15 min billed] |
+--------------------------------------------------+
```

- Focus trap inside modal; initial focus on Description.
- Client/Project default to MRU; dropdown supports typeahead.
- Duration accepts `20m`, `1.5h`, `2h 15m`.
- Save button label dynamically shows rounded result.

---

## Screen 1 — Dashboard

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Good morning, Maya                                 Unbilled this week   |
|                                                     +----------------+   |
|                                                     |   8h 45m       |   |
|                                                     |  6 entries     |   |
|                                                     +----------------+   |
|                                                                         |
|  +------------------------+  +------------------------+                 |
|  | Start a timer          |  | Create invoice         |                 |
|  | [Start timer]          |  | [New invoice]          |                 |
|  +------------------------+  +------------------------+                 |
|                                                                         |
|  Recent unbilled time                    [View all]                     |
|  ┌────────────────────────────────────────────────────────────┐        |
|  │ □ Client      │ Project           │ Description       │ Duration │  |
|  ├────────────────────────────────────────────────────────────┤        |
|  │ □ Acme Corp   │ Website Redesign  │ Hero copy revision│ 0h 30m   │  |
|  │ □ Acme Corp   │ Website Redesign  │ Nav spacing fix   │ 0h 15m   │  |
|  │ □ Stark LLC   │ Brand audit       │ Kickoff call      │ 1h 00m   │  |
|  └────────────────────────────────────────────────────────────┘        |
|  [Select all]  [Create invoice for selected (3)]                        |
|                                                                         |
|  Outstanding invoices                                                 |
|  ┌────────────────────────────────────────────────────────────┐        |
|  │ Invoice #   │ Client      │ Due        │ Total   │ Status  │        |
|  ├────────────────────────────────────────────────────────────┤        |
|  │ INV-0004    │ Acme Corp   │ Jun 25     │ $1,200  │ Sent    │        |
|  │ INV-0003    │ Stark LLC   │ Jun 18     │ $850    │ Overdue │        |
|  └────────────────────────────────────────────────────────────┘        |
|                                                                         |
+-------------------------------------------------------------------------+
```

### Notes

- Dashboard is the default landing view after login.
- Unbilled card is the highest-contrast module to reinforce the bet outcome.
- Checkbox column on the time table lets users start invoicing directly from the dashboard.

---

## Screen 2 — Time tracker

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Time tracker                              [+ Log time] [Start timer]   |
|                                                                         |
|  Filters: [All clients ▼] [All projects ▼] [Unbilled ▼] [Date range]    |
|                                                                         |
|  ┌────────────────────────────────────────────────────────────────┐    |
|  │ □ │ Date     │ Client      │ Project         │ Description  │ Dur.│ |
|  ├────────────────────────────────────────────────────────────────┤    |
|  │ □ │ Today    │ Acme Corp   │ Website Redesign│ Hero copy    │ 0h30│ |
|  │   │          │             │                 │ [Unbilled]   │     │
|  ├────────────────────────────────────────────────────────────────┤    |
|  │ □ │ Today    │ Acme Corp   │ Website Redesign│ Nav spacing  │ 0h15│ │
|  │   │          │             │                 │ [Unbilled]   │     │
|  ├────────────────────────────────────────────────────────────────┤    |
|  │ □ │ Jun 19   │ Stark LLC   │ Brand audit     │ Kickoff call │ 1h00│ │
|  │   │          │             │                 │ [Billed]     │     │
|  └────────────────────────────────────────────────────────────────┘    |
|                                                                         |
|  [Select all unbilled]  [Create invoice for selected (2)]               |
|                                                                         |
|  Showing 1–20 of 47   [< Prev] [1] [2] [3] [Next >]                     |
|                                                                         |
+-------------------------------------------------------------------------+
```

### Notes

- Status badge uses color only as secondary emphasis; shape/text label is always present.
- Bulk actions appear only when at least one row is selected.
- Each row is clickable to open the entry detail/edit panel.

---

## Screen 3 — Invoice list

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Invoices                                    [+ New invoice]             |
|                                                                         |
|  Status: [All ▼]   Client: [All ▼]   Sort: [Due date ▼]                 |
|                                                                         |
|  ┌───────────────────────────────────────────────────────────────┐     |
|  │ Invoice #  │ Client      │ Issue     │ Due      │ Total │ Status │  |
|  ├───────────────────────────────────────────────────────────────┤     |
|  │ INV-0004   │ Acme Corp   │ Jun 14    │ Jun 28   │ $1,200│ Draft  │  |
|  │ INV-0003   │ Stark LLC   │ Jun 04    │ Jun 18   │ $850  │ Overdue│  |
|  │ INV-0002   │ Acme Corp   │ May 28    │ Jun 11   │ $2,400│ Paid   │  |
|  │ INV-0001   │ Wayne Inc   │ May 20    │ Jun 03   │ $600  │ Paid   │  |
|  └───────────────────────────────────────────────────────────────┘     |
|                                                                         |
|  Showing 1–20 of 12                                                     |
|                                                                         |
+-------------------------------------------------------------------------+
```

### Notes

- Clicking a row navigates to invoice detail.
- Status column uses text + icon; color is not the only differentiator.
- Draft invoices show the strongest CTA to **Send** from the list row.

---

## Screen 4 — Invoice detail

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Invoice INV-0004                                          [Edit] [Send]│
|                                                                         |
|  Status: Draft                                                          |
|  ─────────────────────────────────────────────────────────────────────  │
|                                                                         |
|  Bill to:                     From:                                     │
|  Acme Corp                    Maya Chen Design                          │
|  billing@acme.example         maya@example.com                          │
|                                                                         |
|  Issue date: Jun 14, 2026     Due date: Jun 28, 2026                    │
|                                                                         |
|  ┌───────────────────────────────────────────────────────────────┐     |
|  │ Description                    │ Qty    │ Rate    │ Amount     │     |
|  ├───────────────────────────────────────────────────────────────┤     |
|  │ Website Redesign — 8.50 hours  │ 8.50   │ $150.00 │ $1,275.00  │     |
|  └───────────────────────────────────────────────────────────────┘     |
|                                                                  ─────  │
|                                                  Subtotal  $1,275.00    │
|                                                  Total     $1,275.00    │
|                                                                         │
|  Notes: Net 14. Thank you!                                              │
|                                                                         │
|  ─────────────────────────────────────────────────────────────────────  │
|  [Download PDF]  [Duplicate]  [Cancel invoice]        [Record payment ▼]│
|                                                                         │
+-------------------------------------------------------------------------+
```

### Notes

- Action buttons adapt to status:
  - **Draft:** primary = Send, secondary = Edit.
  - **Sent:** primary = Record payment, secondary = Send reminder.
  - **Paid:** primary disabled, secondary = Download PDF / Duplicate.
- **Record payment** opens a small dialog to choose method and date.
- Line-item descriptions are derived from the linked time entries but editable before send.

---

## Responsive behavior

| Breakpoint | Behavior |
|---|---|
| `≥1024px` | Full table layouts, quick-entry modal centered, timer pill bottom-right. |
| `768–1023px` | Tables remain but hide less critical columns (Issue date, Project) behind a **Show details** row expansion. |
| `<768px` | Tables become stacked cards; quick-entry modal becomes full-screen sheet; timer pill becomes a bottom bar. |

---

## Token usage (from `design-system/tokens.json`)

| Element | Token |
|---|---|
| Primary buttons (`+ Log time`, `Send`) | `component.button-primary` |
| Page background | `semantic.color.background` |
| Surface cards / table stripes | `semantic.color.surface` |
| Primary text | `semantic.color.text-primary` |
| Secondary text / hints | `semantic.color.text-secondary` |
| Danger / overdue / discard | `semantic.color.danger` |
| Interactive links / focus ring | `semantic.color.interactive` |
| Border radius | `global.radius.md` |
| Font family | `global.font.sans` |
