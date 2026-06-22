export type TimeEntryStatus = 'unbilled' | 'billed' | 'written_off'

export interface TimeEntry {
  id: string
  tenant_id: string
  client_id: string
  project_id: string
  invoice_id: string | null
  description: string
  duration_minutes: number
  rounded_minutes: number
  status: TimeEntryStatus
  started_at: string | null
  ended_at: string | null
  created_at: string
  updated_at: string
}

export interface TimeEntryCreate {
  client_id: string
  project_id: string
  description: string
  duration_minutes?: number
  started_at?: string
  ended_at?: string
}

export interface TimeEntryUpdate {
  description?: string
  duration_minutes?: number
}
