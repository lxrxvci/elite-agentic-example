import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import NewProjectPage from '@/page-views/projects-new'

export default function NewProjectRoute() {
  return (
    <ProtectedRoute>
      <NewProjectPage />
    </ProtectedRoute>
  )
}
