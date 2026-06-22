export type InvoiceStatus = 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled'

export interface Money {
  amount: string
  currency: string
}

export interface InvoiceLineItem {
  id: string
  description: string
  quantity: string
  rate: string
  amount: Money
  time_entry_ids: string[]
}

export interface Invoice {
  id: string
  tenant_id: string
  client_id: string
  status: InvoiceStatus
  issue_date: string
  due_date: string
  notes: string | null
  subtotal: Money
  tax: Money
  total: Money
  idempotency_key: string | null
  line_items: InvoiceLineItem[]
  created_at: string
  updated_at: string
}

export interface InvoiceCreate {
  client_id: string
  time_entry_ids: string[]
  issue_date: string
  due_date: string
  notes?: string
  idempotency_key?: string
}

export interface MarkPaidInput {
  payment_method: string
  paid_at?: string
}
