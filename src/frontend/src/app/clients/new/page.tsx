import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import NewClientPage from '@/page-views/clients-new'

export default function NewClientRoute() {
  return (
    <ProtectedRoute>
      <NewClientPage />
    </ProtectedRoute>
  )
}
