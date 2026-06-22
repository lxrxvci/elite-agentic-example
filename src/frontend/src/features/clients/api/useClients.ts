import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { PaginatedResponse } from '@/shared/api/types'
import type { Client } from '@/entities/client/model'

interface UseClientsOptions {
  limit?: number
  offset?: number
}

export function useClients({ limit = 100, offset = 0 }: UseClientsOptions = {}) {
  return useQuery<PaginatedResponse<Client>>({
    queryKey: ['clients', limit, offset],
    queryFn: () => apiClient(`/clients?limit=${limit}&offset=${offset}`),
  })
}
