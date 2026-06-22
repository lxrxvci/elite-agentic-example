export interface Client {
  id: string
  tenant_id: string
  name: string
  email: string | null
  currency: string
  default_hourly_rate: string | null
  created_at: string
  updated_at: string
}

export interface ClientCreate {
  name: string
  email?: string
  currency?: string
  default_hourly_rate?: string
}
