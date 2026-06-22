import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { Client, ClientCreate } from '@/entities/client/model'

export function useCreateClient() {
  const queryClient = useQueryClient()
  return useMutation<Client, Error, ClientCreate>({
    mutationFn: (payload) => apiClient('/clients', { method: 'POST', body: JSON.stringify(payload) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clients'] }),
  })
}
