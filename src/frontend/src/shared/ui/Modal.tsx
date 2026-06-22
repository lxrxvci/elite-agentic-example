'use client'

import { useEffect, useRef, type ReactNode } from 'react'
import { Button } from './Button'

interface ModalProps {
  open: boolean
  onClose: () => void
  title: string
  children: ReactNode
  footer?: ReactNode
}

export function Modal({ open, onClose, title, children, footer }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (open) {
      dialog.showModal()
    } else {
      dialog.close()
    }
  }, [open])

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    const handleCancel = (event: Event) => {
      event.preventDefault()
      onClose()
    }
    dialog.addEventListener('cancel', handleCancel)
    return () => dialog.removeEventListener('cancel', handleCancel)
  }, [onClose])

  return (
    <dialog
      ref={dialogRef}
      className="m-auto w-full max-w-lg rounded-lg bg-elite-white p-6 shadow-modal backdrop:bg-black/50"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="flex items-start justify-between gap-4">
        <h2 id="modal-title" className="text-xl font-bold text-elite-text-primary">
          {title}
        </h2>
        <Button variant="ghost" size="sm" onClick={onClose} aria-label="Close dialog">
          ✕
        </Button>
      </div>
      <div className="mt-4">{children}</div>
      {footer && <div className="mt-6 flex justify-end gap-3">{footer}</div>}
    </dialog>
  )
}
