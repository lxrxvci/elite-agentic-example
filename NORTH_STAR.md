# North Star Metric

## Primary Metric

**Monthly Paid Invoice Value (MPIV)** — the total dollar value of invoices created in the dashboard that are marked as paid within the same calendar month.

## Sub-metrics

1. **Median Time-to-Payment (MTP)** — number of days between invoice sent and payment received. Captures the "get paid faster" promise.
2. **Weekly Active Billers (WAB)** — unique freelancers who log at least one billable hour or send at least one invoice in a week. Signals engagement with the core workflow.
3. **Invoice-to-Payment Conversion Rate** — share of sent invoices that are paid within 30 days. Measures trust and usefulness of the billing flow.
4. **Average Invoice Value (AIV)** — median value of invoices sent per user cohort. Helps distinguish casual users from serious freelancers.

## Rationale

`Monthly Paid Invoice Value` is the single best measure of value creation for this product because it directly reflects the freelancer’s reason for showing up: turning time into money. The brief explicitly states the goal is to help freelancers "track time, invoice clients, and get paid faster," and MPIV compresses all three activities into one outcome. Unlike raw signups or logins, it rewards usage that produces a real economic result for the customer, which also correlates with the business’s revenue potential through payment processing, subscription upgrades, or transaction fees.

The sub-metrics act as diagnostic levers rather than competing goals. If MPIV stalls, we can quickly determine whether the bottleneck is low engagement (WAB), slow collections (MTP), payment friction (conversion rate), or user maturity (AIV). Together they keep the team focused on outcomes freelancers actually care about while surfacing where product investment is most likely to move the North Star.
