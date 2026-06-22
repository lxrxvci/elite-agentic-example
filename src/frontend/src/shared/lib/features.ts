let _featureFlags: Record<string, boolean> = {}

export function setFeatureFlags(flags: Record<string, boolean>) {
  _featureFlags = flags
}

export function isFeatureEnabled(flag: string): boolean {
  if (typeof _featureFlags === 'object' && flag in _featureFlags) {
    return _featureFlags[flag]
  }

  if (typeof window === 'undefined') return false

  const flags = (process.env.NEXT_PUBLIC_ENABLED_FEATURES || '')
    .split(',')
    .map((f) => f.trim())
    .filter(Boolean)
  return flags.includes(flag)
}
