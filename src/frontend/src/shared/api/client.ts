import { useAuthStore } from '@/features/auth/model/store'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface ProblemDetail {
  type?: string
  title: string
  status: number
  detail?: string
  errors?: Array<{ loc: string[]; msg: string; type: string }>
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public problem?: ProblemDetail
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export async function apiClient<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = useAuthStore.getState().token
  const url = `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const problem: ProblemDetail = {
      title: body.title || `HTTP ${response.status}`,
      status: response.status,
      detail: body.detail,
      type: body.type,
      errors: body.errors,
    }
    throw new ApiError(problem.detail || problem.title, response.status, problem)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}
