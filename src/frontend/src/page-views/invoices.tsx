'use client'

import Link from 'next/link'
import { useInvoices } from '@/features/invoices/api/useInvoices'
import { Button, EmptyState, InvoiceCard } from '@/shared/ui'

export default function InvoicesPage() {
  const { data: invoices, isLoading } = useInvoices()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-elite-text-primary">Invoices</h1>
        <Link href="/invoices/new">
          <Button>+ Create invoice</Button>
        </Link>
      </div>

      {isLoading ? (
        <p className="text-elite-text-secondary">Loading…</p>
      ) : invoices?.items.length ? (
        <div className="grid gap-4 md:grid-cols-2">
          {invoices.items.map((invoice) => (
            <Link key={invoice.id} href={`/invoices/${invoice.id}`}>
              <InvoiceCard invoice={invoice} />
            </Link>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No invoices yet"
          description="Create your first invoice from unbilled time entries."
          actionLabel="Create invoice"
          onAction={() => {}}
        />
      )}
    </div>
  )
}
