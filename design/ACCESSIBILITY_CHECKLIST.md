# Accessibility Checklist — Bet 1: Capture More Billable Hours

*WCAG 2.1 AA compliance checklist for the key screens and global components introduced in this bet. Each item must be verified by the UI Technologist and Frontend Engineer during build, and spot-checked in the usability test.*

---

## Global components

### Quick-entry modal

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 1.1 | Modal is triggered by `Cmd/Ctrl + Shift + T` and by the nav button. | Manual keyboard test on macOS and Windows. | Frontend |
| 1.2 | Focus moves into the modal when opened and is trapped inside until closed. | Tab through all fields; verify focus does not leave modal. | Frontend |
| 1.3 | Initial focus lands on the **Description** field. | Screen-reader announcement check. | Frontend |
| 1.4 | Closing the modal returns focus to the element that triggered it. | Keyboard-only test. | Frontend |
| 1.5 | `aria-labelledby` references the modal title; `aria-describedby` references helper text. | Inspect accessibility tree. | Frontend |
| 1.6 | Form fields have associated `<label>` elements, not just placeholders. | Automated a11y scan. | Frontend |
| 1.7 | Inline validation errors are linked with `aria-describedby` and announced by `aria-live="polite"`. | Trigger errors with screen reader active. | Frontend |
| 1.8 | Color alone is not used to indicate state (e.g., invalid fields have text + icon). | Visual inspection in grayscale. | UX / Frontend |
| 1.9 | Shortcut hint is available as tooltip text and `aria-description`. | Screen-reader check. | Frontend |

### Live timer floating indicator

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 2.1 | Timer controls are reachable by keyboard (`Tab`) and operable with `Enter`/`Space`. | Keyboard-only test. | Frontend |
| 2.2 | Elapsed time is announced every 15 minutes via `aria-live="polite"`, not every second. | Screen-reader observation. | Frontend |
| 2.3 | Button labels change from **Start timer** to **Stop timer** and are announced. | Inspect `aria-label` updates. | Frontend |
| 2.4 | Timer has sufficient color contrast against all page backgrounds. | Contrast checker (`#2563eb` on `#ffffff` ≥ 4.5:1). | Frontend |

### Top navigation

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 3.1 | All nav items are reachable by `Tab` and activatable by `Enter`. | Keyboard-only test. | Frontend |
| 3.2 | Current page is indicated by `aria-current="page"` and not color alone. | Inspect accessibility tree. | Frontend |
| 3.3 | User menu trigger has `aria-expanded` and `aria-controls`. | Screen-reader / a11y scan. | Frontend |

---

## Screen 1 — Dashboard

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 4.1 | Heading hierarchy starts at `<h1>` and is sequential. | Automated scan. | Frontend |
| 4.2 | **Unbilled this week** summary is announced as a live region when it changes. | Add an entry and verify announcement. | Frontend |
| 4.3 | Table column headers use `<th scope="col">` and row checkboxes have `aria-label="Select entry"`. | Inspect DOM. | Frontend |
| 4.4 | Status badges include visible text label (e.g., “Unbilled”) and are not icon-only. | Visual + screen-reader check. | UX / Frontend |
| 4.5 | Bulk action bar appears after row selection and receives focus. | Keyboard + screen-reader test. | Frontend |
| 4.6 | All text meets 4.5:1 contrast on surface backgrounds. | Contrast checker. | Frontend |
| 4.7 | Dashboard cards maintain logical focus order: summary → quick actions → recent time → outstanding invoices. | Tab order test. | Frontend |

---

## Screen 2 — Time tracker

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 5.1 | Filter dropdowns have visible labels and `aria-label` when collapsed. | Inspect DOM. | Frontend |
| 5.2 | Table rows are keyboard navigable and each row links to detail with a unique accessible name. | Tab through rows. | Frontend |
| 5.3 | Sortable columns expose sort state with `aria-sort` and button labels. | Screen-reader check. | Frontend |
| 5.4 | Pagination controls announce current page and total pages. | Inspect `aria-label` on pagination. | Frontend |
| 5.5 | Empty state (no time entries) is announced and provides a clear next action. | Delete all entries / use test account. | Frontend |
| 5.6 | Bulk action buttons are disabled until selection and announce state. | Keyboard + screen reader. | Frontend |

---

## Screen 3 — Invoice list

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 6.1 | Status filter uses a native `<select>` or accessible custom listbox with `aria-expanded`/`aria-selected`. | Screen-reader / a11y scan. | Frontend |
| 6.2 | Invoice status is conveyed by text + icon; color is secondary. | Grayscale inspection. | UX / Frontend |
| 6.3 | Row actions (Send, Record payment) are accessible by keyboard and have descriptive labels. | Tab to each action. | Frontend |
| 6.4 | Overdue status is announced with `aria-live="polite"` on first load if present. | Screen-reader observation. | Frontend |
| 6.5 | Sort and filter changes update `aria-live` region with result count. | Screen-reader check. | Frontend |

---

## Screen 4 — Invoice detail

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 7.1 | Invoice title uses `<h1>`; status is a subheading, not only a color badge. | Automated scan + visual. | Frontend |
| 7.2 | Primary action changes based on status (Draft → Send, Sent → Record payment, Paid → disabled) and is announced. | Screen-reader check. | Frontend |
| 7.3 | Line-item table uses `<table>` semantics with `<th scope="col">`. | Inspect DOM. | Frontend |
| 7.4 | Monetary values are announced clearly by screen readers (e.g., “one thousand two hundred dollars” depending on SR settings). | Screen-reader check. | Frontend |
| 7.5 | **Record payment** dialog traps focus, has a labelled title, and returns focus to the trigger on close. | Keyboard test. | Frontend |
| 7.6 | Payment method `<select>` has an associated `<label>`. | Automated scan. | Frontend |
| 7.7 | After marking paid, a success message is announced and the status badge updates. | Screen-reader + visual test. | Frontend |

---

## Cross-screen color & contrast

| # | Requirement | How to verify | Owner |
|---|---|---|---|
| 8.1 | All text ≥ 4.5:1 against its background (3:1 for large text ≥ 18pt or 14pt bold). | Contrast checker on every text/background pair. | Frontend |
| 8.2 | Interactive elements (buttons, links, inputs) have a visible focus indicator using `semantic.color.interactive` (`#2563eb`). | Keyboard tab test. | Frontend |
| 8.3 | Error text uses `semantic.color.danger` (`#dc2626`) plus icon and explanatory text. | Grayscale + screen-reader check. | Frontend |
| 8.4 | Information is not conveyed by color alone (e.g., status badges, overdue rows). | Design review + grayscale inspection. | UX |

---

## Keyboard focus order reference

1. Page load → skip-link → nav logo → nav links → **+ Log time** → user menu.
2. Open quick-entry modal → Client → Project → Description → Duration → Save → Cancel.
3. Start timer → timer pill gets focus → Stop → Description in modal → Save.
4. Dashboard time table → select all checkbox → row checkboxes → row links → bulk actions.
5. Invoice create → client/project filters → entry checkboxes → date inputs → notes → Create draft.
6. Invoice detail → Send/Record payment → line items (read-only) → secondary actions.

---

## Screen reader labels — key strings

| Element | Suggested accessible label |
|---|---|
| `+ Log time` button | “Log time, keyboard shortcut Control Shift T” |
| Quick-entry modal | “Log time dialog” |
| Duration input | “Duration, for example 20 minutes or 1.5 hours” |
| Live timer start | “Start timer” |
| Live timer stop | “Stop timer at 1 hour 15 minutes” |
| Timer discard | “Discard timer” |
| Row checkbox | “Select entry, Acme Corp, Website Redesign, Hero copy revision, 30 minutes” |
| Status badge — Unbilled | “Unbilled” |
| Status badge — Billed | “Billed” |
| Record payment button | “Record payment for invoice INV-0004” |
| Mark paid confirm | “Payment recorded. Invoice status is now paid.” |

---

## Sign-off

| Role | Name | Date | Notes |
|---|---|---|---|
| UX Designer |  |  |  |
| UI Technologist |  |  |  |
| Frontend Engineer |  |  |  |
