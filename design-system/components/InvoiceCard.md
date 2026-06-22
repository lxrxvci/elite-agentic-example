# InvoiceCard

Row or stacked card representing an invoice. Used in the invoice list, dashboard “Outstanding invoices”, and mobile stacked layouts.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `invoiceNumber` | `string` | — | e.g. `INV-0004`. |
| `clientName` | `string` | — | Client name. |
| `issueDate` | `string` | — | Display issue date. |
| `dueDate` | `string` | — | Display due date. |
| `total` | `Money` | — | `{ amount, currency }`. |
| `status` | `'draft' \| 'sent' \| 'paid' \| 'overdue' \| 'cancelled'` | — | Invoice status. |
| `layout` | `'row' \| 'stacked'` | `'row'` | Table row or mobile card. |
| `primaryAction` | `{ label, onClick }` | — | Status-specific primary action. |
| `secondaryActions` | `{ label, onClick }[]` | `[]` | Additional actions. |
| `onClick` | `() => void` | — | Navigate to invoice detail. |

## Usage

- Invoice list rows.
- Dashboard outstanding invoices.
- Mobile <768px stacked cards.

## Tokens

| Element | Token / value |
|---|---|
| Background | `semantic.color.background` |
| Border | `semantic.color.border` (proposed) |
| Hover bg | `semantic.color.surface` |
| Overdue accent | left border `semantic.color.danger` |
| Radius | `global.radius.md` |
| Title text | `semantic.color.text-primary`, `weight-medium` |
| Meta text | `semantic.color.text-secondary`, `size-sm` |
| Total | `semantic.color.text-primary`, `weight-bold` |

## Behavior

- Entire card/row is clickable and navigates to detail.
- Primary action changes by status: **Send** (draft), **Record payment** (sent/overdue), disabled (paid).
- Mobile stacked layout reorders fields: status top-right, total prominent, due date emphasized.

## Accessibility

- Row layout uses semantic `<tr>` inside a `<table>`.
- Action buttons have descriptive labels including invoice number, e.g. *“Send invoice INV-0004”*.
- Overdue status conveyed by text, badge, and left danger border — not color alone.
- Total amount is announced clearly by screen readers.
