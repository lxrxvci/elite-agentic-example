import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { PaginatedResponse } from '@/shared/api/types'
import type { Invoice } from '@/entities/invoice/model'

interface UseInvoicesOptions {
  status?: Invoice['status']
  clientId?: string
  limit?: number
  offset?: number
}

export function useInvoices({
  status,
  clientId,
  limit = 100,
  offset = 0,
}: UseInvoicesOptions = {}) {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) })
  if (status) params.set('status', status)
  if (clientId) params.set('client_id', clientId)
  return useQuery<PaginatedResponse<Invoice>>({
    queryKey: ['invoices', status, clientId, limit, offset],
    queryFn: () => apiClient(`/invoices?${params.toString()}`),
  })
}
