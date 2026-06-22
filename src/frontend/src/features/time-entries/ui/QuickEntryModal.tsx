'use client'

import { useMemo, useState } from 'react'
import { Button, Input, Modal, Select, Textarea, useToast } from '@/shared/ui'
import { useClients } from '@/features/clients/api/useClients'
import { useProjects } from '@/features/projects/api/useProjects'
import { useCreateTimeEntry } from '../api/useCreateTimeEntry'

interface QuickEntryModalProps {
  open: boolean
  onClose: () => void
}

export function QuickEntryModal({ open, onClose }: QuickEntryModalProps) {
  const { data: clients } = useClients()
  const [clientId, setClientId] = useState('')
  const [projectId, setProjectId] = useState('')
  const [description, setDescription] = useState('')
  const [durationMinutes, setDurationMinutes] = useState('')
  const { toast } = useToast()
  const create = useCreateTimeEntry()

  const clientOptions = useMemo(() => {
    const options = (clients?.items || []).map((c) => ({ value: c.id, label: c.name }))
    return [{ value: '', label: 'Select client' }, ...options]
  }, [clients])

  const { data: projects } = useProjects({ clientId: clientId || undefined })
  const projectOptions = useMemo(() => {
    const options = (projects?.items || []).map((p) => ({ value: p.id, label: p.name }))
    return [{ value: '', label: 'Select project' }, ...options]
  }, [projects])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!clientId || !projectId || !description || !durationMinutes) return
    try {
      await create.mutateAsync({
        client_id: clientId,
        project_id: projectId,
        description,
        duration_minutes: Number(durationMinutes),
      })
      toast('Time entry logged', 'success')
      setClientId('')
      setProjectId('')
      setDescription('')
      setDurationMinutes('')
      onClose()
    } catch (err) {
      toast(err instanceof Error ? err.message : 'Failed to log time', 'error')
    }
  }

  const footer = (
    <>
      <Button type="button" variant="secondary" onClick={onClose}>
        Cancel
      </Button>
      <Button type="submit" form="quick-entry-form" loading={create.isPending}>
        Log time
      </Button>
    </>
  )

  return (
    <Modal open={open} onClose={onClose} title="Quick time entry" footer={footer}>
      <form id="quick-entry-form" onSubmit={handleSubmit} className="space-y-4">
        <Select
          label="Client"
          value={clientId}
          onChange={(e) => {
            setClientId(e.target.value)
            setProjectId('')
          }}
          options={clientOptions}
          required
        />
        <Select
          label="Project"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          options={projectOptions}
          required
        />
        <Textarea
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          required
        />
        <Input
          label="Duration (minutes)"
          type="number"
          min={1}
          value={durationMinutes}
          onChange={(e) => setDurationMinutes(e.target.value)}
          required
        />
      </form>
    </Modal>
  )
}
