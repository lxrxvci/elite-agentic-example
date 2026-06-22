'use client'

import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from 'react'

interface Toast {
  id: string
  message: string
  variant?: 'success' | 'error' | 'info'
}

interface ToastContextValue {
  toast: (message: string, variant?: Toast['variant']) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const toast = useCallback((message: string, variant: Toast['variant'] = 'info') => {
    const id = `${Date.now()}-${Math.random()}`
    setToasts((prev) => [...prev, { id, message, variant }])
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 4000)
  }, [])

  const remove = (id: string) => setToasts((prev) => prev.filter((t) => t.id !== id))

  const variantClasses: Record<NonNullable<Toast['variant']>, string> = {
    success: 'bg-green-600 text-white',
    error: 'bg-elite-danger text-white',
    info: 'bg-elite-gray-900 text-white',
  }

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div
        className="fixed bottom-4 right-4 z-50 flex flex-col gap-2"
        aria-live="polite"
        aria-atomic="true"
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            className={[
              'rounded-md px-4 py-2 shadow-card',
              variantClasses[t.variant || 'info'],
            ].join(' ')}
          >
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium">{t.message}</span>
              <button
                onClick={() => remove(t.id)}
                className="text-xs underline opacity-80 hover:opacity-100"
                aria-label="Dismiss notification"
              >
                Dismiss
              </button>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}
