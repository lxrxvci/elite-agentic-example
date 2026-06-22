import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { Invoice } from '@/entities/invoice/model'

export function useInvoice(id: string) {
  return useQuery<Invoice>({
    queryKey: ['invoice', id],
    queryFn: () => apiClient(`/invoices/${id}`),
    enabled: Boolean(id),
  })
}
