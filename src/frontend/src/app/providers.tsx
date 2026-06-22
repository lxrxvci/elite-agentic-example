'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import { FeatureFlagsProvider } from '@/shared/lib/FeatureFlagsProvider'

function parseEnvFlags(): Record<string, boolean> {
  if (typeof window === 'undefined') return {}
  return (process.env.NEXT_PUBLIC_ENABLED_FEATURES || '')
    .split(',')
    .map((f) => f.trim())
    .filter(Boolean)
    .reduce<Record<string, boolean>>((acc, flag) => {
      acc[flag] = true
      return acc
    }, {})
}

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <QueryClientProvider client={queryClient}>
      <FeatureFlagsProvider fallbackFlags={parseEnvFlags()}>
        {children}
      </FeatureFlagsProvider>
    </QueryClientProvider>
  )
}
