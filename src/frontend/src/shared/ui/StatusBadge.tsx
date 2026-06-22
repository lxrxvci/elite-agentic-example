type BadgeStatus =
  | 'unbilled'
  | 'billed'
  | 'written_off'
  | 'draft'
  | 'sent'
  | 'paid'
  | 'overdue'
  | 'cancelled'

type BadgeSize = 'sm' | 'md'

interface StatusBadgeProps {
  status: BadgeStatus
  size?: BadgeSize
  icon?: 'none' | 'leading'
}

const statusConfig: Record<
  BadgeStatus,
  { label: string; bg: string; text: string }
> = {
  unbilled: { label: 'Unbilled', bg: 'bg-blue-600/10', text: 'text-elite-blue-600' },
  billed: { label: 'Billed', bg: 'bg-elite-surface', text: 'text-elite-text-secondary' },
  written_off: { label: 'Written off', bg: 'bg-elite-surface', text: 'text-elite-text-secondary' },
  draft: { label: 'Draft', bg: 'bg-elite-surface', text: 'text-elite-text-secondary' },
  sent: { label: 'Sent', bg: 'bg-amber-600/10', text: 'text-elite-warning' },
  paid: { label: 'Paid', bg: 'bg-green-600/10', text: 'text-elite-success' },
  overdue: { label: 'Overdue', bg: 'bg-red-600/10', text: 'text-elite-danger' },
  cancelled: { label: 'Cancelled', bg: 'bg-elite-surface', text: 'text-elite-text-secondary' },
}

const sizeClasses: Record<BadgeSize, string> = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
}

export function StatusBadge({ status, size = 'md', icon = 'leading' }: StatusBadgeProps) {
  const config = statusConfig[status]
  return (
    <span
      className={[
        'inline-flex items-center gap-1.5 rounded-md font-medium',
        config.bg,
        config.text,
        sizeClasses[size],
      ].join(' ')}
    >
      {icon === 'leading' && (
        <span className="h-1.5 w-1.5 rounded-full bg-current" aria-hidden="true" />
      )}
      {config.label}
    </span>
  )
}
