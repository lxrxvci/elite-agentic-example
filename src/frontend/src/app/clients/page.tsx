import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import ClientsPage from '@/page-views/clients'

export default function ClientsRoute() {
  return (
    <ProtectedRoute>
      <ClientsPage />
    </ProtectedRoute>
  )
}
