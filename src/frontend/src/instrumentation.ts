import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({
    serviceName: process.env.NEXT_PUBLIC_UNLEASH_APP_NAME || 'elite-frontend',
  })
}
