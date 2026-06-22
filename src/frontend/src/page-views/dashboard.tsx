'use client'

import { useState } from 'react'
import { useTimeEntries } from '@/features/time-entries/api/useTimeEntries'
import { QuickEntryModal } from '@/features/time-entries/ui/QuickEntryModal'
import { LiveTimerPill } from '@/features/time-entries/ui/LiveTimerPill'
import { useClients } from '@/features/clients/api/useClients'
import { useProjects } from '@/features/projects/api/useProjects'
import { Button, EmptyState, TimeEntryRow, UnbilledSummaryCard } from '@/shared/ui'
import { isFeatureEnabled } from '@/shared/lib/features'

export function DashboardPage() {
  const [quickOpen, setQuickOpen] = useState(false)
  const { data: entries, isLoading } = useTimeEntries({ status: 'unbilled', limit: 5 })
  const { data: clients } = useClients()
  const firstClient = clients?.items[0]
  const { data: projects } = useProjects({ clientId: firstClient?.id })
  const firstProject = projects?.items[0]

  const totalMinutes = entries?.items.reduce((sum, e) => sum + e.rounded_minutes, 0) || 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-elite-text-primary">Dashboard</h1>
        <div className="flex items-center gap-3">
          {isFeatureEnabled('time-capture.live-timer') && (
            <LiveTimerPill
              clientId={firstClient?.id || ''}
              projectId={firstProject?.id || ''}
              description="Timed work"
            />
          )}
          {isFeatureEnabled('time-capture.quick-entry') && (
            <Button onClick={() => setQuickOpen(true)}>+ Log time</Button>
          )}
        </div>
      </div>

      <UnbilledSummaryCard
        totalMinutes={totalMinutes}
        entryCount={entries?.total || 0}
      />

      <section aria-label="Recent unbilled entries">
        <h2 className="mb-3 text-lg font-bold text-elite-text-primary">Recent unbilled entries</h2>
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
            title="No unbilled time yet"
            description="Log your first time entry to see it here."
            actionLabel="Log time"
            onAction={() => setQuickOpen(true)}
          />
        )}
      </section>

      <QuickEntryModal open={quickOpen} onClose={() => setQuickOpen(false)} />
    </div>
  )
}
