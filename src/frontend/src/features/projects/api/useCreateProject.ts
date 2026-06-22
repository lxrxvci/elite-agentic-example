import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { Project, ProjectCreate } from '@/entities/project/model'

export function useCreateProject() {
  const queryClient = useQueryClient()
  return useMutation<Project, Error, ProjectCreate>({
    mutationFn: (payload) => apiClient('/projects', { method: 'POST', body: JSON.stringify(payload) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['projects'] }),
  })
}
