import { ProtectedRoute } from '@/features/auth/ui/ProtectedRoute'
import NewInvoicePage from '@/page-views/invoices-new'

export default function NewInvoiceRoute() {
  return (
    <ProtectedRoute>
      <NewInvoicePage />
    </ProtectedRoute>
  )
}
