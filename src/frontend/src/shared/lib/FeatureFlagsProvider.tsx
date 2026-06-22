'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { UnleashClient, type IConfig } from 'unleash-proxy-client'
import { setFeatureFlags } from './features'

type FeatureFlagsContextValue = Record<string, boolean>

const FeatureFlagsContext = createContext<FeatureFlagsContextValue>({})

interface FeatureFlagsProviderProps {
  children: ReactNode
  fallbackFlags?: Record<string, boolean>
}

export function FeatureFlagsProvider({ children, fallbackFlags = {} }: FeatureFlagsProviderProps) {
  const [flags, setFlags] = useState<FeatureFlagsContextValue>(fallbackFlags)

  useEffect(() => {
    const proxyUrl = process.env.NEXT_PUBLIC_UNLEASH_PROXY_URL
    if (!proxyUrl) {
      setFeatureFlags(fallbackFlags)
      return
    }

    const config: IConfig = {
      url: proxyUrl,
      clientKey: process.env.NEXT_PUBLIC_UNLEASH_CLIENT_KEY || 'default:development.unleash-insecure-api-token',
      refreshInterval: 15,
      appName: process.env.NEXT_PUBLIC_UNLEASH_APP_NAME || 'elite-frontend',
      environment: process.env.NEXT_PUBLIC_VERCEL_ENV || 'development',
    }

    const client = new UnleashClient(config)

    const updateFlags = () => {
      const enabledFlags = client.getAllToggles().reduce<Record<string, boolean>>((acc, toggle) => {
        acc[toggle.name] = toggle.enabled
        return acc
      }, fallbackFlags)
      setFlags(enabledFlags)
      setFeatureFlags(enabledFlags)
    }

    client.on('ready', updateFlags)
    client.on('update', updateFlags)
    client.start()

    return () => {
      client.stop()
    }
  }, [fallbackFlags])

  return <FeatureFlagsContext.Provider value={flags}>{children}</FeatureFlagsContext.Provider>
}

export function useFeatureFlags(): FeatureFlagsContextValue {
  return useContext(FeatureFlagsContext)
}
