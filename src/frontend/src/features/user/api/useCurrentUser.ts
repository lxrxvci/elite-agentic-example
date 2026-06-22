import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/shared/api/client'
import type { User } from '@/entities/user/model'

export function useCurrentUser() {
  return useQuery<User>({
    queryKey: ['me'],
    queryFn: () => apiClient('/me'),
  })
}
