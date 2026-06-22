import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { Invoice, InvoiceCreate } from '@/entities/invoice/model'

export function useCreateInvoice() {
  const queryClient = useQueryClient()
  return useMutation<Invoice, Error, InvoiceCreate>({
    mutationFn: (payload) =>
      apiClient('/invoices', { method: 'POST', body: JSON.stringify(payload) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
      queryClient.invalidateQueries({ queryKey: ['time-entries'] })
    },
  })
}
