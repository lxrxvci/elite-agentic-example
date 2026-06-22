'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/shared/ui'
import { useCreateTimeEntry } from '../api/useCreateTimeEntry'

const STORAGE_KEY = 'elite-live-timer'

interface TimerState {
  running: boolean
  startedAt: string
  description: string
  clientId: string
  projectId: string
}

interface LiveTimerPillProps {
  clientId: string
  projectId: string
  description: string
}

export function LiveTimerPill({ clientId, projectId, description }: LiveTimerPillProps) {
  const [state, setState] = useState<TimerState | null>(null)
  const [elapsed, setElapsed] = useState(0)
  const create = useCreateTimeEntry()

  useEffect(() => {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) {
      try {
        setState(JSON.parse(raw))
      } catch {
        sessionStorage.removeItem(STORAGE_KEY)
      }
    }
  }, [])

  useEffect(() => {
    if (!state?.running) return
    const interval = setInterval(() => {
      const start = new Date(state.startedAt).getTime()
      setElapsed(Math.floor((Date.now() - start) / 1000))
    }, 1000)
    return () => clearInterval(interval)
  }, [state])

  const start = () => {
    const next: TimerState = {
      running: true,
      startedAt: new Date().toISOString(),
      description,
      clientId,
      projectId,
    }
    setState(next)
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next))
    setElapsed(0)
  }

  const stop = async () => {
    if (!state) return
    const minutes = Math.max(1, Math.round(elapsed / 60))
    try {
      await create.mutateAsync({
        client_id: state.clientId,
        project_id: state.projectId,
        description: state.description || 'Timed work',
        duration_minutes: minutes,
      })
    } finally {
      setState(null)
      sessionStorage.removeItem(STORAGE_KEY)
      setElapsed(0)
    }
  }

  const formatElapsed = (seconds: number) => {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = seconds % 60
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  if (state?.running) {
    return (
      <div className="flex items-center gap-3 rounded-full bg-elite-interactive px-4 py-2 text-white shadow-card">
        <span className="relative flex h-3 w-3">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-white opacity-75 motion-reduce:animate-none" />
          <span className="relative inline-flex h-3 w-3 rounded-full bg-white" />
        </span>
        <span className="font-mono text-sm">{formatElapsed(elapsed)}</span>
        <Button variant="ghost" size="sm" className="text-white hover:bg-white/10" onClick={stop} loading={create.isPending}>
          Stop
        </Button>
      </div>
    )
  }

  const disabled = !clientId || !projectId
  return (
    <Button
      size="sm"
      onClick={start}
      disabled={disabled}
      title={disabled ? 'Select a client and project first' : 'Start timer'}
    >
      Start timer
    </Button>
  )
}
