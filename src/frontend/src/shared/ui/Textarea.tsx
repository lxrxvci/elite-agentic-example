import { forwardRef, type TextareaHTMLAttributes } from 'react'

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, className = '', id, ...props }, ref) => {
    const textId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)
    return (
      <div className={className}>
        {label && (
          <label htmlFor={textId} className="mb-1 block text-sm font-medium text-elite-text-primary">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textId}
          className={[
            'w-full rounded-md border px-3 py-2 text-base text-elite-text-primary',
            'placeholder:text-elite-text-secondary',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-elite-interactive focus-visible:ring-offset-2',
            error ? 'border-elite-danger' : 'border-elite-border',
          ].join(' ')}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${textId}-error` : undefined}
          {...props}
        />
        {error && (
          <p id={`${textId}-error`} className="mt-1 text-sm text-elite-danger">
            {error}
          </p>
        )}
      </div>
    )
  }
)
Textarea.displayName = 'Textarea'
