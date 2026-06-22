import { Button } from './Button'

interface EmptyStateProps {
  title: string
  description?: string
  actionLabel?: string
  onAction?: () => void
  illustration?: 'none' | 'document' | 'clock'
}

export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
  illustration = 'none',
}: EmptyStateProps) {
  return (
    <section
      className="flex flex-col items-center justify-center rounded-lg border border-elite-border bg-elite-background p-6 text-center"
      aria-live="polite"
    >
      {illustration !== 'none' && (
        <div className="mb-4 text-elite-text-secondary" aria-hidden="true">
          {illustration === 'document' ? (
            <svg className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          ) : (
            <svg className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          )}
        </div>
      )}
      <h2 className="text-lg font-bold text-elite-text-primary">{title}</h2>
      {description && (
        <p className="mt-1 text-base text-elite-text-secondary">{description}</p>
      )}
      {actionLabel && onAction && (
        <Button className="mt-4" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </section>
  )
}
