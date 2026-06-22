import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { TimeEntry, TimeEntryCreate } from '@/entities/time-entry/model'

export function useCreateTimeEntry() {
  const queryClient = useQueryClient()
  return useMutation<TimeEntry, Error, TimeEntryCreate>({
    mutationFn: (payload) =>
      apiClient('/time-entries', { method: 'POST', body: JSON.stringify(payload) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['time-entries'] })
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
    },
  })
}
