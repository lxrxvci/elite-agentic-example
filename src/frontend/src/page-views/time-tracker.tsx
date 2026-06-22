'use client'

import { useState } from 'react'
import { useTimeEntries } from '@/features/time-entries/api/useTimeEntries'
import { QuickEntryModal } from '@/features/time-entries/ui/QuickEntryModal'
import { Button, EmptyState, TimeEntryRow } from '@/shared/ui'
import { isFeatureEnabled } from '@/shared/lib/features'

export default function TimeTrackerPage() {
  const [status, setStatus] = useState<'all' | 'unbilled' | 'billed'>('all')
  const [quickOpen, setQuickOpen] = useState(false)
  const { data: entries, isLoading } = useTimeEntries({
    status: status === 'all' ? undefined : status,
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-elite-text-primary">Time tracker</h1>
        {isFeatureEnabled('time-capture.quick-entry') && (
          <Button onClick={() => setQuickOpen(true)}>+ Log time</Button>
        )}
      </div>

      <div className="flex gap-2">
        {(['all', 'unbilled', 'billed'] as const).map((s) => (
          <Button
            key={s}
            variant={status === s ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setStatus(s)}
          >
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </Button>
        ))}
      </div>

      {isLoading ? (
        <p className="text-elite-text-secondary">Loading…</p>
      ) : entries?.items.length ? (
        <div className="space-y-3">
          {entries.items.map((entry) => (
            <TimeEntryRow
              key={entry.id}
              description={entry.description}
              durationMinutes={entry.duration_minutes}
              roundedMinutes={entry.rounded_minutes}
              status={entry.status}
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="No time entries yet"
          description="Start tracking time to see entries here."
          actionLabel="Log time"
          onAction={() => setQuickOpen(true)}
        />
      )}

      <QuickEntryModal open={quickOpen} onClose={() => setQuickOpen(false)} />
    </div>
  )
}
