'use client'

import { useState } from 'react'
import { Button, Input, Modal, useToast } from '@/shared/ui'
import { useMarkInvoicePaid } from '../api/useMarkInvoicePaid'

interface RecordPaymentDialogProps {
  invoiceId: string
  open: boolean
  onClose: () => void
}

export function RecordPaymentDialog({ invoiceId, open, onClose }: RecordPaymentDialogProps) {
  const [method, setMethod] = useState('Bank transfer')
  const markPaid = useMarkInvoicePaid()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await markPaid.mutateAsync({
        id: invoiceId,
        payload: { payment_method: method, paid_at: new Date().toISOString() },
      })
      toast('Invoice marked as paid', 'success')
      onClose()
    } catch (err) {
      toast(err instanceof Error ? err.message : 'Failed to record payment', 'error')
    }
  }

  const footer = (
    <>
      <Button type="button" variant="secondary" onClick={onClose}>
        Cancel
      </Button>
      <Button type="submit" form="record-payment-form" loading={markPaid.isPending}>
        Mark paid
      </Button>
    </>
  )

  return (
    <Modal open={open} onClose={onClose} title="Record payment" footer={footer}>
      <form id="record-payment-form" onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Payment method"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          required
        />
      </form>
    </Modal>
  )
}
