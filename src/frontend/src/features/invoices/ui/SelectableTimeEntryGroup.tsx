import { useMemo } from 'react'
import type { TimeEntry } from '@/entities/time-entry/model'

interface SelectableTimeEntryGroupProps {
  entries: TimeEntry[]
  selectedIds: string[]
  onChange: (selectedIds: string[]) => void
}

export function SelectableTimeEntryGroup({
  entries,
  selectedIds,
  onChange,
}: SelectableTimeEntryGroupProps) {
  const totalMinutes = useMemo(() => {
    return entries
      .filter((e) => selectedIds.includes(e.id))
      .reduce((sum, e) => sum + e.rounded_minutes, 0)
  }, [entries, selectedIds])

  const toggle = (id: string) => {
    onChange(
      selectedIds.includes(id) ? selectedIds.filter((x) => x !== id) : [...selectedIds, id]
    )
  }

  const formatMinutes = (m: number) => {
    const hours = Math.floor(m / 60)
    const mins = m % 60
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`
  }

  return (
    <div className="space-y-2">
      {entries.map((entry) => (
        <label
          key={entry.id}
          className="flex cursor-pointer items-center justify-between rounded-md border border-elite-border bg-elite-white p-3 hover:bg-elite-surface"
        >
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={selectedIds.includes(entry.id)}
              onChange={() => toggle(entry.id)}
              className="h-4 w-4 rounded border-elite-border text-elite-interactive focus-visible:ring-elite-interactive"
            />
            <div>
              <p className="font-medium text-elite-text-primary">{entry.description}</p>
              <p className="text-xs text-elite-text-secondary">
                {formatMinutes(entry.duration_minutes)} tracked
              </p>
            </div>
          </div>
          <span className="text-sm font-medium text-elite-text-primary">
            {formatMinutes(entry.rounded_minutes)}
          </span>
        </label>
      ))}
      <p className="text-right text-sm text-elite-text-secondary">
        Selected: <span className="font-medium text-elite-text-primary">{formatMinutes(totalMinutes)}</span>
      </p>
    </div>
  )
}
