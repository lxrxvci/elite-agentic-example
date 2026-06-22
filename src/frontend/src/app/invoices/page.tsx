import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import InvoicesPage from '@/page-views/invoices'

export default function InvoicesRoute() {
  return (
    <ProtectedRoute>
      <InvoicesPage />
    </ProtectedRoute>
  )
}
