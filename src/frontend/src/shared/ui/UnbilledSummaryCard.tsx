interface UnbilledSummaryCardProps {
  totalMinutes: number
  entryCount: number
  hourlyRate?: number
}

export function UnbilledSummaryCard({
  totalMinutes,
  entryCount,
  hourlyRate = 150,
}: UnbilledSummaryCardProps) {
  const hours = totalMinutes / 60
  const estimatedValue = hours * hourlyRate

  return (
    <div className="rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
      <h2 className="text-lg font-bold text-elite-text-primary">Unbilled time</h2>
      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-4xl font-bold text-elite-text-primary">{hours.toFixed(1)}</span>
        <span className="text-elite-text-secondary">hours across {entryCount} entries</span>
      </div>
      <p className="mt-2 text-sm text-elite-text-secondary">
        Estimated value:{' '}
        <span className="font-medium text-elite-text-primary">
          ${estimatedValue.toFixed(2)}
        </span>{' '}
        at ${hourlyRate}/hr
      </p>
    </div>
  )
}
