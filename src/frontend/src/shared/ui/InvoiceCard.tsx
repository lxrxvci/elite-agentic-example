import { StatusBadge } from './StatusBadge'
import type { Invoice, InvoiceStatus } from '@/entities/invoice/model'

interface InvoiceCardProps {
  invoice: Invoice
  clientName?: string
}

export function InvoiceCard({ invoice, clientName }: InvoiceCardProps) {
  return (
    <div className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-elite-text-secondary">
            {clientName || invoice.client_id}
          </p>
          <p className="text-lg font-bold text-elite-text-primary">
            {invoice.total.currency} {invoice.total.amount}
          </p>
          <p className="text-sm text-elite-text-secondary">
            Issued {invoice.issue_date} · Due {invoice.due_date}
          </p>
        </div>
        <StatusBadge status={invoice.status as InvoiceStatus} />
      </div>
    </div>
  )
}
