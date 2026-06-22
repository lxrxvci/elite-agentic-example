import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import TimeTrackerPage from '@/page-views/time-tracker'

export default function TimeTrackerRoute() {
  return (
    <ProtectedRoute>
      <TimeTrackerPage />
    </ProtectedRoute>
  )
}
