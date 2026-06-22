# InvoiceLineItemTable

Read-only table of invoice line items. Used on the invoice detail screen.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `lineItems` | `InvoiceLineItem[]` | `[]` | Line items to render. |
| `currency` | `string` | — | ISO currency code for formatting. |
| `subtotal` | `Money` | — | Invoice subtotal. |
| `total` | `Money` | — | Invoice total. |

## Usage

- Invoice detail screen.
- Print/PDF preview.

## Tokens

| Element | Token / value |
|---|---|
| Table header text | `semantic.color.text-secondary`, `size-sm`, `weight-medium` |
| Row text | `semantic.color.text-primary`, `size-base` |
| Border | `semantic.color.border` (proposed) |
| Numeric alignment | right |
| Total row | `weight-bold`, `size-lg` |
| Description column | left-aligned, max-width fluid |

## Behavior

- Line items are derived from linked time entries but editable before send.
- Monetary values formatted with currency symbol and two decimals.
- Total row separated by a top border.

## Accessibility

- Use semantic `<table>` with `<thead>`, `<tbody>`, `<th scope="col">`.
- Monetary values in `<td>`; right-aligned visually.
- Total announced clearly by screen readers.
- If line items are editable, each row includes labeled inputs with `aria-describedby` pointing to column headers.
