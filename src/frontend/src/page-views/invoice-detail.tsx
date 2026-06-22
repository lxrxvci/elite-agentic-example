'use client'

import { useState } from 'react'
import { useParams } from 'next/navigation'
import { useInvoice } from '@/features/invoices/api/useInvoice'
import { RecordPaymentDialog } from '@/features/invoices/ui/RecordPaymentDialog'
import { Button, InvoiceLineItemTable, StatusBadge } from '@/shared/ui'

export default function InvoiceDetailPage() {
  const params = useParams()
  const id = typeof params.id === 'string' ? params.id : ''
  const { data: invoice, isLoading } = useInvoice(id)
  const [payOpen, setPayOpen] = useState(false)

  if (isLoading) return <p className="text-elite-text-secondary">Loading…</p>
  if (!invoice) return <p className="text-elite-text-secondary">Invoice not found.</p>

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-elite-text-secondary">Invoice</p>
          <h1 className="text-2xl font-bold text-elite-text-primary">
            {invoice.total.currency} {invoice.total.amount}
          </h1>
          <div className="mt-2">
            <StatusBadge status={invoice.status} />
          </div>
        </div>
        {invoice.status !== 'paid' && invoice.status !== 'cancelled' && (
          <Button onClick={() => setPayOpen(true)}>Record payment</Button>
        )}
      </div>

      <div className="grid gap-4 rounded-lg border border-elite-border bg-elite-white p-6 shadow-card md:grid-cols-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-elite-text-secondary">Issue date</p>
          <p className="font-medium text-elite-text-primary">{invoice.issue_date}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wide text-elite-text-secondary">Due date</p>
          <p className="font-medium text-elite-text-primary">{invoice.due_date}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wide text-elite-text-secondary">Total</p>
          <p className="font-medium text-elite-text-primary">
            {invoice.total.currency} {invoice.total.amount}
          </p>
        </div>
      </div>

      {invoice.notes && (
        <div className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
          <p className="text-sm text-elite-text-secondary">{invoice.notes}</p>
        </div>
      )}

      <div className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
        <h2 className="mb-4 text-lg font-bold text-elite-text-primary">Line items</h2>
        <InvoiceLineItemTable lineItems={invoice.line_items} />
      </div>

      <RecordPaymentDialog invoiceId={invoice.id} open={payOpen} onClose={() => setPayOpen(false)} />
    </div>
  )
}
