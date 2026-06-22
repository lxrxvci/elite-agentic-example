# Interview Synthesis

*Simulated synthesis of three customer discovery interviews conducted in Week 1 of the discovery loop.*

---

## Interviewees

| ID | Role | Revenue | Current stack | Interview goal |
|----|------|---------|---------------|----------------|
| I1 | UX consultant, solo | ~$95k/year | Calendar, Notion, FreshBooks, Zelle | Validate invoicing friction and payment follow-up pain |
| I2 | Full-stack developer, 4 clients | ~$130k/year | Toggl, GitHub issues, Wave, PayPal | Validate time-capture gaps and embedded payment desire |
| I3 | Brand strategist, retained clients | ~$115k/year | Harvest, Google Sheets, Stripe, email | Validate cash-flow visibility and reminder psychology |

---

## Key Quotes

### On time capture
> “I bill every two weeks, but by Friday I’ve already forgotten the 20-minute fixes I did on Tuesday.” — I2

> “The best tool would be the one that captures time without me thinking about it. I hate starting a timer.” — I1

### On invoicing
> “Creating the invoice isn’t the hard part. Remembering everything that should be on it is.” — I3

> “I have a template, but I still spend 15 minutes checking that my hours match the project.” — I2

### On payments and follow-up
> “I once waited 60 days because I was too embarrassed to remind a client. It was $8,000.” — I1

> “If the system sent the reminder, I could blame the system. That would actually help me.” — I3

> “I can see they opened the invoice in Wave, but it doesn’t tell me if they’re about to pay or ignoring it.” — I2

### On visibility
> “My biggest fear is that I’ll realize on the 30th that half my expected income for the month isn’t coming in.” — I3

> “I have a spreadsheet called ‘Who Owes Me’ and I still don’t trust it.” — I1

---

## Patterns

1. **Time capture is fragmented and memory-dependent.**
   All three interviewees rely on calendar memory or batch reconstruction. None consistently use a live timer. The gap is not the absence of a timer — it is the absence of ambient capture from tools they already use.

2. **Invoice creation is psychologically harder than technically hard.**
   The time spent creating an invoice is modest, but anxiety about accuracy and completeness makes freelancers procrastinate. The real pain is fear of under-billing or looking sloppy.

3. **Payment follow-up is emotionally loaded.**
   Freelancers delay follow-ups because reminders feel personal and jeopardize relationships. Automated, system-owned reminders are welcome if the tone is professional.

4. **Cash-flow visibility reduces anxiety more than cash-flow volume.**
   Interviewees did not complain about total earnings; they complained about not knowing when money would arrive. A reliable “who owes what” view is a high-value reassurance tool.

5. **Embedded payment is a trust signal, not just a convenience.**
   Clients paying directly from the invoice shortens the loop and makes the freelancer look more established.

---

## Validated Opportunities

### O1. Reduce the time and effort to create an invoice
**Confidence:** High — all three interviewees described reconstructing billable work and double-checking invoices.
**Evidence:** Quotes from I2 and I3; observed use of spreadsheets and template checks.

### O2. Reduce days between invoice sent and payment received
**Confidence:** High — late payments are a recurring, emotionally costly problem.
**Evidence:** 60-day overdue story (I1); desire for system-owned reminders (I3); read-receipt frustration (I2).

### O3. Capture more billable hours that are currently lost
**Confidence:** High — all interviewees admitted to forgotten micro-tasks and out-of-scope work.
**Evidence:** “20-minute fixes” quote (I2); out-of-scope tasks quote (I1); desire for ambient capture (I1, I3).

### O4. Increase confidence in who owes what and when
**Confidence:** High — cash-flow uncertainty is a direct source of stress.
**Evidence:** “Who Owes Me” spreadsheet (I1); month-end fear (I3); manual reconciliation across tools (I3).

### O5. Reduce the friction of accepting payments inside the product
**Confidence:** Medium — desired by all, but payment method constraints depend on client preference.
**Evidence:** Embedded payment seen as professional (I2, I3); current use of PayPal/Zelle/Stripe indicates willingness to route payments digitally.

### O6. De-personalize payment reminders while preserving the client relationship *(new)*
**Confidence:** Medium-High — emerged strongly across interviews.
**Evidence:** “I could blame the system” (I3); embarrassment around 60-day delay (I1); read-receipt ambiguity (I2). This is a distinct opportunity from automated reminders: it is about emotional cover and tone, not just automation.
