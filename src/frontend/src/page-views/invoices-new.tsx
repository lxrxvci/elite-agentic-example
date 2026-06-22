'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useClients } from '@/features/clients/api/useClients'
import { useCreateInvoice } from '@/features/invoices/api/useCreateInvoice'
import { SelectableTimeEntryGroup } from '@/features/invoices/ui/SelectableTimeEntryGroup'
import { Button, Input, Select, useToast } from '@/shared/ui'
import { useTimeEntries } from '@/features/time-entries/api/useTimeEntries'

export default function NewInvoicePage() {
  const router = useRouter()
  const { data: clients } = useClients()
  const [clientId, setClientId] = useState('')
  const { data: entries } = useTimeEntries({
    status: 'unbilled',
    clientId: clientId || undefined,
  })
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [issueDate, setIssueDate] = useState(() => new Date().toISOString().split('T')[0])
  const [dueDate, setDueDate] = useState(() => {
    const d = new Date()
    d.setDate(d.getDate() + 14)
    return d.toISOString().split('T')[0]
  })
  const [notes, setNotes] = useState('')
  const create = useCreateInvoice()
  const { toast } = useToast()

  const clientOptions = useMemo(() => {
    const options = (clients?.items || []).map((c) => ({ value: c.id, label: c.name }))
    return [{ value: '', label: 'Select client' }, ...options]
  }, [clients])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!clientId || selectedIds.length === 0) return
    try {
      const invoice = await create.mutateAsync({
        client_id: clientId,
        time_entry_ids: selectedIds,
        issue_date: issueDate,
        due_date: dueDate,
        notes: notes || undefined,
        idempotency_key: `${clientId}-${Date.now()}`,
      })
      toast('Invoice created', 'success')
      router.push(`/invoices/${invoice.id}`)
    } catch (err) {
      toast(err instanceof Error ? err.message : 'Failed to create invoice', 'error')
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-elite-text-primary">Create invoice</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <Select
          label="Client"
          value={clientId}
          onChange={(e) => {
            setClientId(e.target.value)
            setSelectedIds([])
          }}
          options={clientOptions}
          required
        />

        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Issue date"
            type="date"
            value={issueDate}
            onChange={(e) => setIssueDate(e.target.value)}
            required
          />
          <Input
            label="Due date"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            required
          />
        </div>

        <Input
          label="Notes (optional)"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <div>
          <h2 className="mb-2 text-lg font-bold text-elite-text-primary">Unbilled time entries</h2>
          {entries?.items.length ? (
            <SelectableTimeEntryGroup
              entries={entries.items}
              selectedIds={selectedIds}
              onChange={setSelectedIds}
            />
          ) : (
            <p className="text-elite-text-secondary">
              {clientId ? 'No unbilled entries for this client.' : 'Select a client to see entries.'}
            </p>
          )}
        </div>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="secondary" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" loading={create.isPending} disabled={selectedIds.length === 0}>
            Create invoice
          </Button>
        </div>
      </form>
    </div>
  )
}
