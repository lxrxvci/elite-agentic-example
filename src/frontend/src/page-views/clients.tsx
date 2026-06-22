'use client'

import Link from 'next/link'
import { useClients } from '@/features/clients/api/useClients'
import { Button, EmptyState } from '@/shared/ui'

export default function ClientsPage() {
  const { data: clients, isLoading } = useClients()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-elite-text-primary">Clients</h1>
        <Link href="/clients/new">
          <Button>+ Add client</Button>
        </Link>
      </div>

      {isLoading ? (
        <p className="text-elite-text-secondary">Loading…</p>
      ) : clients?.items.length ? (
        <div className="grid gap-4 md:grid-cols-2">
          {clients.items.map((client) => (
            <div
              key={client.id}
              className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card"
            >
              <h2 className="text-lg font-bold text-elite-text-primary">{client.name}</h2>
              {client.email && (
                <p className="text-sm text-elite-text-secondary">{client.email}</p>
              )}
              <p className="text-sm text-elite-text-secondary">
                Currency: {client.currency}
                {client.default_hourly_rate && ` · ${client.default_hourly_rate}/hr`}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No clients yet"
          description="Add your first client so you can track time and invoice them."
          actionLabel="Add client"
          onAction={() => {}}
        />
      )}
    </div>
  )
}
