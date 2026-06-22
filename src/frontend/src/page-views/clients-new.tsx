'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useCreateClient } from '@/features/clients/api/useCreateClient'
import { Button, Input, Select, useToast } from '@/shared/ui'

const currencies = ['USD', 'EUR', 'GBP', 'CAD']

export default function NewClientPage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [currency, setCurrency] = useState('USD')
  const [rate, setRate] = useState('')
  const create = useCreateClient()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await create.mutateAsync({
        name,
        email,
        currency,
        default_hourly_rate: rate || undefined,
      })
      toast('Client created', 'success')
      router.push('/clients')
    } catch (err) {
      toast(err instanceof Error ? err.message : 'Failed to create client', 'error')
    }
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <h1 className="text-2xl font-bold text-elite-text-primary">Add client</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
        <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Select
          label="Currency"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          options={currencies.map((c) => ({ value: c, label: c }))}
        />
        <Input
          label="Default hourly rate"
          type="number"
          step="0.01"
          value={rate}
          onChange={(e) => setRate(e.target.value)}
        />
        <div className="flex justify-end gap-3 pt-2">
          <Button type="button" variant="secondary" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" loading={create.isPending}>
            Save client
          </Button>
        </div>
      </form>
    </div>
  )
}
