import { forwardRef, type SelectHTMLAttributes } from 'react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: { value: string; label: string }[]
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, options, className = '', id, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)
    return (
      <div className={className}>
        {label && (
          <label htmlFor={selectId} className="mb-1 block text-sm font-medium text-elite-text-primary">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={[
            'w-full rounded-md border bg-elite-white px-3 py-2 text-base text-elite-text-primary',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-elite-interactive focus-visible:ring-offset-2',
            error ? 'border-elite-danger' : 'border-elite-border',
          ].join(' ')}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${selectId}-error` : undefined}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && (
          <p id={`${selectId}-error`} className="mt-1 text-sm text-elite-danger">
            {error}
          </p>
        )}
      </div>
    )
  }
)
Select.displayName = 'Select'
