import type { InvoiceLineItem } from '@/entities/invoice/model'

interface InvoiceLineItemTableProps {
  lineItems: InvoiceLineItem[]
}

export function InvoiceLineItemTable({ lineItems }: InvoiceLineItemTableProps) {
  return (
    <table className="w-full text-left text-sm">
      <thead className="border-b border-elite-border text-elite-text-secondary">
        <tr>
          <th className="py-2 font-medium">Description</th>
          <th className="py-2 font-medium">Qty</th>
          <th className="py-2 font-medium">Rate</th>
          <th className="py-2 text-right font-medium">Amount</th>
        </tr>
      </thead>
      <tbody>
        {lineItems.map((item) => (
          <tr key={item.id} className="border-b border-elite-border last:border-0">
            <td className="py-3 text-elite-text-primary">{item.description}</td>
            <td className="py-3 text-elite-text-secondary">{item.quantity}</td>
            <td className="py-3 text-elite-text-secondary">
              {item.amount.currency} {item.rate}
            </td>
            <td className="py-3 text-right font-medium text-elite-text-primary">
              {item.amount.currency} {item.amount.amount}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
