import { forwardRef, type InputHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)
    return (
      <div className={className}>
        {label && (
          <label htmlFor={inputId} className="mb-1 block text-sm font-medium text-elite-text-primary">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={[
            'w-full rounded-md border px-3 py-2 text-base text-elite-text-primary',
            'placeholder:text-elite-text-secondary',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-elite-interactive focus-visible:ring-offset-2',
            error ? 'border-elite-danger' : 'border-elite-border',
          ].join(' ')}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${inputId}-error` : undefined}
          {...props}
        />
        {error && (
          <p id={`${inputId}-error`} className="mt-1 text-sm text-elite-danger">
            {error}
          </p>
        )}
      </div>
    )
  }
)
Input.displayName = 'Input'
