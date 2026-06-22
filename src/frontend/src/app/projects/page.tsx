import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import ProjectsPage from '@/page-views/projects'

export default function ProjectsRoute() {
  return (
    <ProtectedRoute>
      <ProjectsPage />
    </ProtectedRoute>
  )
}
