# Usability Test Plan — Bet 1: Capture More Billable Hours

*Lightweight, unmoderated-or-moderated usability validation to run before engineering handoff. Target participants: 3–5 freelancers matching the ICP ($50k–$150k, 2–10 clients, currently use spreadsheets or generic tools).*

---

## Goals

1. Validate that a freelancer can log a manual time entry in under 10 seconds in a realistic context-switching scenario.
2. Confirm the live timer is discoverable, trustworthy, and easy to convert into a saved entry.
3. Verify that converting unbilled hours into an invoice does not feel slower or more complex than the user’s current workflow.
4. Catch accessibility blockers (keyboard, screen reader, color) before high-fidelity polish.

---

## Method

- **Format:** 30-minute moderated remote sessions via video call + screen share, OR unmoderated task recordings (e.g. Maze, UserTesting).
- **Prototype fidelity:** Text-based clickable wireframes / low-fidelity prototype in the design tool.
- **Scoring:** Each task is pass/fail/partial. Target is ≥80% pass rate per task before handoff.
- **Think-aloud:** Encourage participants to verbalize confusion, distrust, or surprise.

---

## Tasks & success criteria

### Task 1 — Log a micro-task in the middle of another workflow

**Scenario:** You just finished a 20-minute revision a client asked for in Slack. You are currently looking at a different client’s invoice. Log this work without losing your place.

**Steps to observe:**
1. Participant discovers and uses the quick-entry shortcut or nav button.
2. Enters client, project, description, and duration.
3. Saves and returns to the previous screen.

**Success criteria:**
- **Pass:** Completes in ≤10 seconds (excluding typing the description) and does not navigate away from the invoice screen.
- **Partial:** Completes but uses the full Time tracker page instead of the quick-entry widget.
- **Fail:** Cannot find how to log time, or abandons the task.

**Follow-up questions:**
- Did the default client/project match what you expected?
- Was the duration format (`20m`, `1.5h`) obvious?

---

### Task 2 — Start a timer, stop it, and save the entry

**Scenario:** You are about to start a 45-minute focused work block. Use the live timer, then save the captured time.

**Steps to observe:**
1. Participant starts the timer from the dashboard or quick-entry modal.
2. Performs a short distractor task (e.g. read a paragraph).
3. Stops the timer and saves the resulting entry.

**Success criteria:**
- **Pass:** Starts timer without hesitation, stops it, and saves the pre-filled entry.
- **Partial:** Saves but edits the rounded duration because it feels wrong.
- **Fail:** Cannot locate the timer control, or loses the elapsed time before saving.

**Follow-up questions:**
- Did the floating timer stay visible enough while you worked?
- Did the rounded duration feel fair?

---

### Task 3 — Turn unbilled hours into an invoice

**Scenario:** It is Friday afternoon. You have several unbilled entries for Acme Corp this week. Create and send an invoice for only those entries.

**Steps to observe:**
1. Participant navigates to invoice creation.
2. Selects only Acme Corp entries.
3. Reviews line items and totals.
4. Sends the invoice.

**Success criteria:**
- **Pass:** Creates a single-client invoice in ≤90 seconds, with correct line items, and sends it.
- **Partial:** Creates invoice but includes wrong entries or takes >90 seconds.
- **Fail:** Cannot figure out how to select entries, or gives up due to complexity.

**Follow-up questions:**
- Did the grouped list match how you think about billing?
- Did you trust that the totals were correct?

---

### Task 4 — Record an offline payment

**Scenario:** Acme Corp just paid you $1,200 via bank transfer. Mark the invoice as paid.

**Steps to observe:**
1. Participant opens the sent invoice.
2. Uses the **Record payment** action.
3. Selects payment method and confirms.

**Success criteria:**
- **Pass:** Records payment and confirms status changed to Paid.
- **Partial:** Finds the action but is unsure which payment method to pick.
- **Fail:** Cannot locate **Record payment**, or attempts to edit the invoice instead.

**Follow-up questions:**
- Did the status change give you confidence the books are correct?
- Would you expect a confirmation email or receipt?

---

### Task 5 — Complete the core loop using only the keyboard

**Scenario:** You are logging time while on a call and cannot use a mouse. Open the quick-entry widget, fill it out, and save using only your keyboard.

**Steps to observe:**
1. Participant uses the keyboard shortcut to open the modal.
2. Navigates fields with `Tab`/`Shift+Tab`.
3. Saves with `Enter`.

**Success criteria:**
- **Pass:** Completes the full flow without touching the mouse and without getting trapped.
- **Partial:** Completes but has trouble with the dropdown or focus order.
- **Fail:** Cannot open the modal or navigate the form by keyboard.

**Follow-up questions:**
- Did the focus order feel natural?
- Were shortcut hints discoverable?

---

## Metrics & decision gate

| Metric | Target | Action if missed |
|---|---|---|
| Task 1 pass rate (≤10 s manual capture) | ≥80% | Revisit shortcut hint, MRU defaults, or duration input parsing. |
| Task 2 pass rate (timer start/stop/save) | ≥80% | Increase timer visibility or change default rounding rule. |
| Task 3 pass rate (invoice creation ≤90 s) | ≥80% | Simplify grouping, selection, or default dates. |
| Task 5 pass rate (keyboard-only) | ≥80% | Fix focus order, focus trap, or shortcut before handoff. |
| System Usability Scale (SUS) | ≥68 | Iterate on clarity and trust signals. |
| Qualitative pain themes | ≤2 severe per session | Document in design decision log and re-test. |

---

## Deliverables after testing

1. **Usability findings summary** — pass/partial/fail table with quotes and video timestamps.
2. **Design iteration log** — changes made to wireframes before handoff.
3. **Accessibility findings** — keyboard/screen-reader issues routed to the UI Technologist.
4. **Go/no-go recommendation** for high-fidelity design and engineering build.
