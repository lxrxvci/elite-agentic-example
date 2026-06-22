import { StatusBadge } from './StatusBadge'

interface TimeEntryRowProps {
  description: string
  durationMinutes: number
  roundedMinutes: number
  status: 'unbilled' | 'billed' | 'written_off'
  clientName?: string
  projectName?: string
}

export function TimeEntryRow({
  description,
  durationMinutes,
  roundedMinutes,
  status,
  clientName,
  projectName,
}: TimeEntryRowProps) {
  const formatMinutes = (m: number) => {
    const hours = Math.floor(m / 60)
    const mins = m % 60
    if (hours === 0) return `${mins}m`
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`
  }

  return (
    <div className="flex items-center justify-between rounded-md border border-elite-border bg-elite-white p-4 shadow-card">
      <div className="min-w-0">
        <p className="truncate font-medium text-elite-text-primary">{description}</p>
        {(clientName || projectName) && (
          <p className="text-sm text-elite-text-secondary">
            {[clientName, projectName].filter(Boolean).join(' · ')}
          </p>
        )}
      </div>
      <div className="flex items-center gap-4">
        <div className="text-right">
          <p className="font-medium text-elite-text-primary">{formatMinutes(roundedMinutes)}</p>
          {roundedMinutes !== durationMinutes && (
            <p className="text-xs text-elite-text-secondary">{formatMinutes(durationMinutes)} tracked</p>
          )}
        </div>
        <StatusBadge status={status} />
      </div>
    </div>
  )
}
