export interface Tenant {
  id: string
  name: string
  default_currency: string
  default_hourly_rate: string | null
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  tenant_id: string
  email: string
  name: string
  tenant: Tenant
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  email: string
}

export interface AuthToken {
  access_token: string
  token_type: string
}
