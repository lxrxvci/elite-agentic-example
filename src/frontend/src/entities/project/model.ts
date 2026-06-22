export interface Project {
  id: string
  tenant_id: string
  client_id: string
  name: string
  rounding_minutes: number
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  client_id: string
  name: string
  rounding_minutes?: number
}
