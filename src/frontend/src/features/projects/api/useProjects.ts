import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { PaginatedResponse } from '@/shared/api/types'
import type { Project } from '@/entities/project/model'

interface UseProjectsOptions {
  clientId?: string
  limit?: number
  offset?: number
}

export function useProjects({ clientId, limit = 100, offset = 0 }: UseProjectsOptions = {}) {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) })
  if (clientId) params.set('client_id', clientId)
  return useQuery<PaginatedResponse<Project>>({
    queryKey: ['projects', clientId, limit, offset],
    queryFn: () => apiClient(`/projects?${params.toString()}`),
  })
}
