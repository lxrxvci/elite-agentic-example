# RecordPaymentDialog

Dialog for recording an offline payment against a sent or overdue invoice.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `isOpen` | `boolean` | — | Controls visibility. |
| `invoiceId` | `string` | — | Invoice being paid. |
| `invoiceNumber` | `string` | — | For labels. |
| `defaultPaidAt` | `string` | — | ISO datetime string defaulting to now. |
| `onClose` | `() => void` | — | Close callback. |
| `onConfirm` | `(payload: InvoiceMarkPaid) => void` | — | Confirm callback. |

## Usage

- Triggered from the invoice detail **Record payment** button.
- Also available in the invoice list row actions when status is `sent` or `overdue`.

## Tokens

| Element | Token / value |
|---|---|
| Overlay | `component.modal.overlay` (proposed) |
| Container bg | `semantic.color.background` |
| Container radius | `global.radius.lg` |
| Container padding | `global.spacing.06` |
| Input tokens | same as `QuickEntryModal` |
| Confirm button | `Button` primary |
| Cancel button | `Button` secondary |

## Behavior

- **Payment method** select is required; options: `bank_transfer`, `card`, `cash`, `check`, `other`.
- **Paid at** defaults to current local datetime; editable.
- On confirm, call `POST /invoices/{id}/mark-paid`, close dialog, and show success toast.
- Mark-paid is disabled on draft invoices (tooltip explains).

## Accessibility

- Use native `<dialog>` with focus trap.
- `aria-labelledby` references the dialog title.
- Labels associated with inputs.
- Return focus to the **Record payment** trigger on close.
- Success message announced via `aria-live="polite"`.
