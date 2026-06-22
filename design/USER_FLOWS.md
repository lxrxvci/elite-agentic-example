# User Flows — Bet 1: Capture More Billable Hours

*Design artifacts for the top shaped bet. Flows assume a first-run user has already created at least one client and project; the empty-state path is noted as an edge case.*

---

## Flow 1 — Log a billable moment in under 10 seconds (manual quick-entry)

**Trigger:** Freelancer finishes a micro-task or out-of-scope request and wants to capture it before context switching.

1. User presses `Cmd/Ctrl + Shift + T` (or clicks the persistent **“Log time”** button in the top nav).
2. Quick-entry modal opens with focus in the **Description** field.
3. **Client** and **Project** default to the most recently used (MRU) pair.
4. User types a short description, e.g. *“Revised homepage hero copy”*.
5. User enters duration as `20m` (or `0.5h`, or `1h 15m`) in the **Duration** field.
6. User presses `Enter` (or clicks **Save**).
7. Modal closes; a toast confirms *“20 minutes logged for Acme Corp — Website Redesign”*.
8. The dashboard **Unbilled this week** card increments by the rounded amount.

### Edge cases & branch logic

| Situation | UX behavior |
|---|---|
| No clients/projects exist yet | Modal shows a compact empty state with **“Add your first client”** primary CTA; no form fields are rendered. |
| MRU client/project is archived or deleted | Defaults fall back to the alphabetically first active client/project; label shown as helper text. |
| Validation fails (empty description, negative duration) | Inline errors appear below offending fields; focus stays in modal; no data is lost. |
| User presses the shortcut while the modal is already open | Toggle closed (escape behavior), preserving partial input for 60 seconds via session state. |
| Server returns 409 duplicate | Toast explains *“This entry looks like a duplicate. Edit or save anyway?”* with an explicit **Save anyway** action. |

---

## Flow 2 — Start a live timer, stop it, and save the entry

**Trigger:** Freelancer begins a focused block of work and wants the system to measure it.

1. User clicks the **Start timer** button (or uses the `Cmd/Ctrl + Shift + T` shortcut and selects **Timer** tab).
2. A floating timer pill appears in the bottom-right corner showing elapsed time rounded display (e.g. `0h 15m`).
3. User works in other tabs/apps; timer keeps running in the active browser session.
4. User returns and clicks **Stop** on the floating pill (or re-opens the modal and clicks **Stop timer**).
5. The quick-entry modal opens pre-filled with:
   - **Client/Project:** MRU pair.
   - **Duration:** elapsed time rounded to the nearest 15 minutes (e.g. 37 min → 45 min).
   - **Description:** empty, focus placed here so the user describes the work.
6. User edits details if needed and clicks **Save**.
7. Timer pill disappears; entry appears in the time tracker with an **Unbilled** badge.

### Edge cases & branch logic

| Situation | UX behavior |
|---|---|
| Browser refreshes while timer is running | On reload, the timer restores from `sessionStorage` using the original start timestamp; a subtle **“Timer recovered”** banner is shown. |
| User closes the tab | Timer state is lost (by design — no multi-device sync). On next login, dashboard shows a gentle **“You had a running timer that was not saved”** recovery card only if the stop event was never received. |
| Elapsed time rounds to `0` minutes | Display `< 15 min` and save as `0` rounded minutes, but show raw duration in the detail view for transparency. |
| User clicks **Discard** instead of Save | Confirm with a non-blocking inline prompt; on confirm, no time entry is created and timer state is cleared. |
| Stop is clicked accidentally | Modal opens pre-filled; user can edit duration down or cancel without saving. |

---

## Flow 3 — Convert unbilled time into a paid invoice

**Trigger:** End of week / billing moment; freelancer wants to invoice captured hours.

1. User navigates to **Invoices** and clicks **New invoice**.
2. Invoice-create screen shows unbilled entries grouped by client/project with selectable rows.
3. User selects one client (e.g. Acme Corp) and one or more entries.
4. System auto-fills:
   - **Issue date:** today.
   - **Due date:** today + 14 days (default Net 14; editable).
   - **Line items:** grouped by project, quantity = rounded hours, rate = tenant default rate.
5. User reviews totals and clicks **Create draft**.
6. System atomically creates the invoice and marks selected entries as **billed**.
7. User is taken to the invoice detail screen.
8. User clicks **Send invoice**; status moves to **sent**.
9. When payment is received offline, user clicks **Record payment**, selects method (bank transfer / Zelle / etc.), and confirms.
10. Status moves to **paid**; dashboard **Unbilled this week** and **Outstanding invoices** update.

### Edge cases & branch logic

| Situation | UX behavior |
|---|---|
| User selects entries from multiple clients | Inline validation appears: *“An invoice can only be for one client. Create separate invoices?”* with one-click **Create invoices for each client**. |
| No unbilled entries exist | New-invoice button opens a blank draft with a helper link back to the time tracker; no grouped list is shown. |
| Selected entry is already billed by another session (409) | Error modal lists the conflict; user can refresh the list to see current state. |
| Default hourly rate is not set | Inline banner: *“Set a default hourly rate in Settings to see invoice totals.”* Form remains submittable with $0.00 totals. |
| Mark-paid is clicked on a draft | Disabled until invoice is sent; tooltip explains *“Send the invoice before recording payment.”* |

---

## Cross-flow principles

- **Always-visible progress:** Unbilled hours and timer state are surfaced on the dashboard and in the nav, reducing the chance of forgotten entries.
- **Atomic handoffs:** When time becomes an invoice line item, the original entry is marked billed in the same transaction so users never accidentally double-bill.
- **Fallback paths:** Every primary action has a clear secondary path (discard, cancel, edit, or try again) to protect against mistakes during evening admin.
