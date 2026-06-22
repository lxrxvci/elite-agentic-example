import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { PaginatedResponse } from '@/shared/api/types'
import type { TimeEntry } from '@/entities/time-entry/model'

interface UseTimeEntriesOptions {
  status?: 'unbilled' | 'billed' | 'written_off'
  clientId?: string
  projectId?: string
  limit?: number
  offset?: number
}

export function useTimeEntries({
  status,
  clientId,
  projectId,
  limit = 100,
  offset = 0,
}: UseTimeEntriesOptions = {}) {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) })
  if (status) params.set('status', status)
  if (clientId) params.set('client_id', clientId)
  if (projectId) params.set('project_id', projectId)
  return useQuery<PaginatedResponse<TimeEntry>>({
    queryKey: ['time-entries', status, clientId, projectId, limit, offset],
    queryFn: () => apiClient(`/time-entries?${params.toString()}`),
  })
}
