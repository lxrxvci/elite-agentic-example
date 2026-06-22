# High-Fidelity Prototypes — Bet 1: Capture More Billable Hours

*Design artifacts for the top shaped bet. All values reference `/design-system/tokens.json` and the proposed token additions documented in `DEV_HANDOFF.md`.*

---

## Global components

### G1. Top navigation

- **Height:** 64px, `semantic.color.background`, 1px bottom border `semantic.color.border` (proposed `#e5e7eb`).
- **Left:** logo mark + app wordmark.
- **Center:** Dashboard · Time tracker · Invoices · Clients. Active item uses `font-weight-medium` + 2px bottom border `semantic.color.interactive`.
- **Right:** primary `+ Log time` button; user avatar trigger.
- **Shortcut hint:** tooltip / `aria-description` on the `+ Log time` button: *“Log time, keyboard shortcut Control Shift T”*.

| State | Visual |
|---|---|
| default | nav links `semantic.color.text-secondary`, bg white |
| hover | nav links `semantic.color.interactive`; primary button bg darkens ~10% |
| active / pressed | primary button bg darkens ~15% |
| focus | 2px outline `semantic.color.interactive`, offset 2px |
| disabled | button opacity 0.5, `cursor: not-allowed` |

---

### G2. Quick-entry modal

A global modal reachable from any screen. Two tabs: **Manual entry** (default) and **Timer**.

- **Container:** max-width `560px`, `semantic.color.background`, `global.radius.lg`, shadow `0 20px 25px -5px rgba(0,0,0,0.1)`, padding `global.spacing.06`.
- **Backdrop:** `rgba(0,0,0,0.5)`.
- **Desktop:** centered. **<768px:** full-screen sheet that slides up from bottom.

**Manual tab layout**
```text
Log time                                    [×]
────────────────────────────────────────────────
Client:   [Acme Corp              ▼]
Project:  [Website Redesign       ▼]

Description
[Revised homepage hero copy                    ]
0/2000

Duration: [20m                 ]  or  [Start timer]

[Cancel]            [Save: 20 min → 15 min billed]
```

- Client/Project defaults to the most recently used (MRU) pair; Project options filter when Client changes.
- Duration accepts `20m`, `1.5h`, `2h 15m`; helper text below: *“e.g. 20m, 1.5h, 2h 15m”*.
- Save button label dynamically shows the rounded result: *“Save: 20 min → 15 min billed”*.

**Timer tab layout**
```text
Timer

        ⏱  1h 15m

[Stop timer]    [Discard]
```
- On **Stop**, the modal switches to the Manual tab with Duration pre-filled and focus placed in Description.

| State | Behavior |
|---|---|
| default | MRU client/project selected; initial focus in Description field |
| hover | input borders shift to `semantic.color.interactive`; buttons darken |
| active / pressed | buttons show active offset |
| focus | focus trapped inside modal; visible ring on every interactive element |
| error | inline error text + icon below offending field; focus stays in modal; `aria-describedby` links error to input |
| empty | if no clients exist, form is replaced by a compact empty state with a primary **“Add your first client”** CTA |
| loading | inputs disabled; Save button shows spinner and `aria-busy="true"` |
| duplicate | non-blocking toast appears: *“This entry looks like a duplicate. Edit or save anyway?”* with **Save anyway** action |

---

### G3. Live timer floating indicator

Always-visible timer surfaced while a live timer is running.

- **Desktop:** fixed pill bottom-right.
- **<768px:** full-width bottom bar.
- **Pill:** white bg, 1px border `semantic.color.border`, `global.radius.lg`, shadow, padding `global.spacing.03` `global.spacing.04`.

```text
+--------------------------------+
| ⏱  1h 15m    [Stop]  [Discard] |
+--------------------------------+
```

| State | Behavior |
|---|---|
| default / running | elapsed time rounds to nearest displayed minute; updates every 60s visually |
| hover | shadow elevates slightly |
| focus | Stop / Discard buttons show focus rings |
| recovered | after browser refresh, a subtle banner reads *“Timer recovered”*; elapsed time continues from original start timestamp |
| < 15 min | display reads *“< 15 min”*; saved as `0` rounded minutes but raw duration shown in detail |

---

### G4. Toast

Used for confirmations, errors, and duplicate warnings.

- **Position:** top-right desktop; top-center mobile.
- **Container:** max-width `360px`, white bg, border, radius `global.radius.md`, shadow.
- **Variants:** success (green icon), error (danger icon), info (interactive icon).
- Auto-dismiss after 5s; pause on hover/focus.

| State | Behavior |
|---|---|
| default | icon + title + message + optional action + dismiss |
| hover / focus | timer pauses; dismiss button focusable |
| action | optional button executes callback without dismissing until complete |

---

## Screen 1 — Dashboard

Default landing view after login.

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Good morning, Maya                       +-------------------------+   |
|                                           │ Unbilled this week      │   |
|                                           │                         │   |
|                                           │        8h 45m           │   |
|                                           │        6 entries        │   |
|                                           +-------------------------+   |
|                                                                         |
|  +-------------------------+  +-------------------------+              |
|  │ ⏱ Start a timer         │  │ 🧾 Create invoice        │              |
|  │ [Start timer]           │  │ [New invoice]            │              |
|  +-------------------------+  +-------------------------+              |
|                                                                         |
|  Recent unbilled time                              [View all]           |
|  ┌────────────────────────────────────────────────────────────┐        |
|  │ □ Client      │ Project           │ Description       │ Duration │  |
|  ├────────────────────────────────────────────────────────────┤        |
|  │ □ Acme Corp   │ Website Redesign  │ Hero copy revision│ 0h 30m   │  |
|  │ □ Acme Corp   │ Website Redesign  │ Nav spacing fix   │ 0h 15m   │  |
|  │ □ Stark LLC   │ Brand audit       │ Kickoff call      │ 1h 00m   │  |
|  └────────────────────────────────────────────────────────────┘        |
|  [Select all]  [Create invoice for selected (3)]                        |
|                                                                         |
|  Outstanding invoices                                                   |
|  ┌────────────────────────────────────────────────────────────┐        |
|  │ Invoice #   │ Client      │ Due        │ Total   │ Status  │        |
|  ├────────────────────────────────────────────────────────────┤        |
|  │ INV-0004    │ Acme Corp   │ Jun 25     │ $1,200  │ Sent    │        |
|  │ INV-0003    │ Stark LLC   │ Jun 18     │ $850    │ Overdue │        |
|  └────────────────────────────────────────────────────────────┘        |
+-------------------------------------------------------------------------+
```

### Visual details

- **Unbilled this week** card: highest-contrast module. `semantic.color.surface` background, `global.radius.lg`, left 4px accent `semantic.color.interactive`. Metric `8h 45m` at `global.font.size-2xl` / `weight-bold`; sublabel `6 entries` at `size-sm` / `text-secondary`.
- **Quick-action cards:** `semantic.color.surface`, radius lg, icon + title + CTA button.
- **Tables:** white rows, 1px row borders `semantic.color.border`, header text `text-secondary` / `size-sm`.
- **Bulk action bar:** appears only when ≥1 row selected; `semantic.color.surface` with top border; primary action disabled until all selected rows share one client.

### States

| State | Behavior |
|---|---|
| default | MRU greeting; latest unbilled entries and outstanding invoices |
| hover | table rows bg shift to `semantic.color.surface`; action buttons darken |
| active | CTA buttons pressed; row click opens detail/edit panel |
| selected | checkbox checked; row shows left accent border |
| empty — no time entries | recent table replaced by EmptyState: *“No unbilled time yet”* + **Log time** CTA |
| empty — no invoices | outstanding table replaced by EmptyState: *“No outstanding invoices”* |
| loading | skeleton cards + skeleton table rows; no interactive elements |
| error | inline error card with retry action; toast on mutations |

---

## Screen 2 — Time tracker

Full history and bulk-invoicing view.

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
|  │ □ │ Today    │ Acme Corp   │ Website Redesign│ Nav spacing  │ 0h15│ │
|  │   │          │             │                 │ [Unbilled]   │     │
|  │ □ │ Jun 19   │ Stark LLC   │ Brand audit     │ Kickoff call │ 1h00│ │
|  │   │          │             │                 │ [Billed]     │     │
|  └────────────────────────────────────────────────────────────────┘    |
|                                                                         |
|  [Select all unbilled]  [Create invoice for selected (2)]               |
|                                                                         |
|  Showing 1–20 of 47   [< Prev] [1] [2] [3] [Next >]                     |
+-------------------------------------------------------------------------+
```

### States

| State | Behavior |
|---|---|
| default | paginated list; status badges show text + color |
| hover | row bg `semantic.color.surface`; description becomes underline link color |
| active | row click opens entry detail / edit panel |
| selected | checkbox checked; bulk action bar appears |
| empty | EmptyState with **Log time** CTA |
| loading | skeleton rows; filters disabled |
| filter changed | pagination resets to page 1; result count announced via `aria-live` |

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
|  │ INV-0003   │ Stark LLC   │ Jun 04    │ Jun 18   │ $850  │ Overdue│  │
|  │ INV-0002   │ Acme Corp   │ May 28    │ Jun 11   │ $2,400│ Paid   │  │
|  │ INV-0001   │ Wayne Inc   │ May 20    │ Jun 03   │ $600  │ Paid   │  │
|  └───────────────────────────────────────────────────────────────┘     |
|                                                                         |
|  Showing 1–20 of 12                                                     |
+-------------------------------------------------------------------------+
```

### States

| State | Behavior |
|---|---|
| default | list sorted by due date; draft rows expose **Send** action |
| hover | row bg surface; action buttons visible/underlined |
| active | row click navigates to invoice detail |
| overdue | row has left danger accent border; status badge = danger |
| empty | EmptyState with **New invoice** CTA |
| loading | skeleton rows |

---

## Screen 4 — Invoice detail

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  Invoice INV-0004                                          [Edit] [Send]│
|  Status: Draft                                                          |
|  ─────────────────────────────────────────────────────────────────────  │
|                                                                         |
|  Bill to:                     From:                                     │
|  Acme Corp                    Maya Chen Design                          │
|  billing@acme.example         maya@example.com                          │
|                                                                         |
|  Issue date: Jun 14, 2026     Due date: Jun 28, 2026                    │
|                                                                         |
|  ┌───────────────────────────────────────────────────────────────┐     │
|  │ Description                    │ Qty    │ Rate    │ Amount     │     │
|  ├───────────────────────────────────────────────────────────────┤     │
|  │ Website Redesign — 8.50 hours  │ 8.50   │ $150.00 │ $1,275.00  │     │
|  └───────────────────────────────────────────────────────────────┘     │
|                                                                  ─────  │
|                                                  Subtotal  $1,275.00    │
|                                                  Total     $1,275.00    │
|                                                                         │
|  Notes: Net 14. Thank you!                                              │
|                                                                         │
|  ─────────────────────────────────────────────────────────────────────  │
|  [Download PDF]  [Duplicate]  [Cancel invoice]        [Record payment ▼]│
+-------------------------------------------------------------------------+
```

### Action adaptations by status

| Status | Primary action | Secondary actions |
|---|---|---|
| Draft | Send invoice | Edit, Download PDF, Duplicate, Cancel |
| Sent | Record payment | Send reminder, Download PDF, Duplicate |
| Paid | disabled / hidden | Download PDF, Duplicate |
| Overdue | Record payment | Send reminder, Download PDF |
| Cancelled | — | Duplicate, Download PDF |

### States

| State | Behavior |
|---|---|
| default | read-only detail; line items editable only before send |
| hover | action buttons darken; line-item rows highlight on hover in edit mode |
| active | **Send** triggers status change + toast; **Record payment** opens dialog |
| loading | action buttons disabled with spinner; totals skeleton |
| error | error card or toast (e.g. conflict) |
| paid success | status badge updates; success toast; totals move to “paid” summary |

---

## Screen 5 — Invoice create

New invoice from unbilled time entries.

```text
+-------------------------------------------------------------------------+
| [Logo]  Dashboard   Time tracker   Invoices   Clients   [+ Log time] [A] |
+-------------------------------------------------------------------------+
|                                                                         |
|  New invoice                                                             |
|                                                                         |
|  Select unbilled time                                                    │
|  ┌────────────────────────────────────────────────────────────────────┐ │
|  │ □ Acme Corp — Website Redesign              3 entries   1h 15m    │ │
|  │   □ Hero copy revision                        0h 30m              │ │
|  │   □ Nav spacing fix                           0h 15m              │ │
|  │   □ Footer links                              0h 30m              │ │
|  └────────────────────────────────────────────────────────────────────┘ │
|                                                                         │
|  +-------------------------------------------------------------+        │
|  │ Invoice summary                                             │        │
|  │ Client: Acme Corp                                           │        │
|  │ Issue date: [Jun 21, 2026]   Due date: [Jul 5, 2026]        │        │
|  │                                                             │        │
|  │ Line items                                                  │        │
|  │ Website Redesign — 1.25 hours          $187.50              │        │
|  │ ─────────────────────────────────────────────────           │        │
|  │ Total                                  $187.50              │        │
|  │                                                             │        │
|  │ Notes                                                       │        │
|  │ [Net 14. Thank you!                               ]         │        │
|  │                                                             │        │
|  │ [Create draft]                                              │        │
|  +-------------------------------------------------------------+        │
+-------------------------------------------------------------------------+
```

### Behavior

- Unbilled entries grouped by client/project; group header checkbox selects all entries in the group.
- Issue date defaults to today; due date defaults to today + 14 days.
- Line items group by project; quantity = rounded hours; rate = tenant default rate.
- If entries from multiple clients are selected, inline validation appears: *“An invoice can only be for one client. Create separate invoices?”* with **Create invoices for each client**.

### States

| State | Behavior |
|---|---|
| default | first client group expanded; no entries selected; totals $0.00 |
| hover | group headers and rows highlight; summary card action buttons darken |
| active | group checkbox toggles all; individual row toggles one |
| multi-client error | validation banner at top of summary; Create draft disabled until resolved |
| empty — no unbilled | EmptyState with link back to Time tracker |
| loading | skeleton groups; summary disabled |

---

## Responsive behavior

| Breakpoint | Behavior |
|---|---|
| `≥1024px` | Full table layouts; quick-entry modal centered; timer pill floating bottom-right. |
| `768–1023px` | Tables remain; less critical columns (Issue date, Project) hidden behind **Show details** expandable row. |
| `<768px` | Tables become stacked cards; quick-entry modal becomes full-screen sheet; timer pill becomes full-width bottom bar. |

---

## Motion & timing

| Transition | Duration | Easing |
|---|---|---|
| Modal enter / exit | 150ms | `ease-out` / `ease-in` |
| Button hover / active | 100ms | `ease` |
| Toast slide + fade | 200ms | `ease-out` |
| Timer pill slide up | 200ms | `ease-out` |
| Table row hover bg | 100ms | `ease` |
| Loading skeleton shimmer | 1.5s | `linear` infinite |
| Focus ring | 0ms | no transition (instant visibility) |

Respect `prefers-reduced-motion`: disable slide/scale animations; keep opacity-only or instant transitions.
