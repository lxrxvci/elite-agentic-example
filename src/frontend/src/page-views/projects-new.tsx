'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useClients } from '@/features/clients/api/useClients'
import { useCreateProject } from '@/features/projects/api/useCreateProject'
import { Button, Input, Select, useToast } from '@/shared/ui'

export default function NewProjectPage() {
  const router = useRouter()
  const { data: clients } = useClients()
  const [clientId, setClientId] = useState('')
  const [name, setName] = useState('')
  const [rounding, setRounding] = useState('15')
  const create = useCreateProject()
  const { toast } = useToast()

  const clientOptions = useMemo(() => {
    const options = (clients?.items || []).map((c) => ({ value: c.id, label: c.name }))
    return [{ value: '', label: 'Select client' }, ...options]
  }, [clients])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await create.mutateAsync({
        client_id: clientId,
        name,
        rounding_minutes: Number(rounding),
      })
      toast('Project created', 'success')
      router.push('/projects')
    } catch (err) {
      toast(err instanceof Error ? err.message : 'Failed to create project', 'error')
    }
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <h1 className="text-2xl font-bold text-elite-text-primary">Add project</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-elite-border bg-elite-white p-6 shadow-card">
        <Select
          label="Client"
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
          options={clientOptions}
          required
        />
        <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <Input
          label="Rounding minutes"
          type="number"
          min={1}
          value={rounding}
          onChange={(e) => setRounding(e.target.value)}
          required
        />
        <div className="flex justify-end gap-3 pt-2">
          <Button type="button" variant="secondary" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" loading={create.isPending}>
            Save project
          </Button>
        </div>
      </form>
    </div>
  )
}
