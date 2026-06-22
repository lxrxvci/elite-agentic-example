import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { Invoice, MarkPaidInput } from '@/entities/invoice/model'

export function useMarkInvoicePaid() {
  const queryClient = useQueryClient()
  return useMutation<Invoice, Error, { id: string; payload: MarkPaidInput }>({
    mutationFn: ({ id, payload }) =>
      apiClient(`/invoices/${id}/mark-paid`, { method: 'POST', body: JSON.stringify(payload) }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
      queryClient.invalidateQueries({ queryKey: ['invoice', variables.id] })
    },
  })
}
