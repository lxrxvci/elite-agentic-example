import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import InvoiceDetailPage from '@/page-views/invoice-detail'

export default function InvoiceDetailRoute() {
  return (
    <ProtectedRoute>
      <InvoiceDetailPage />
    </ProtectedRoute>
  )
}
