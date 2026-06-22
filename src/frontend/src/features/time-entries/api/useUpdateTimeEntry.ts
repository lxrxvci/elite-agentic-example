import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { TimeEntry, TimeEntryUpdate } from '@/entities/time-entry/model'

export function useUpdateTimeEntry() {
  const queryClient = useQueryClient()
  return useMutation<TimeEntry, Error, { id: string; payload: TimeEntryUpdate }>({
    mutationFn: ({ id, payload }) =>
      apiClient(`/time-entries/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['time-entries'] }),
  })
}
