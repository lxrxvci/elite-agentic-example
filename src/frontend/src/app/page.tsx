import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import { DashboardPage } from '@/page-views/dashboard'

export default function Home() {
  return (
    <ProtectedRoute>
      <DashboardPage />
    </ProtectedRoute>
  )
}
