import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest'
import { Pact } from '@pact-foundation/pact'
import path from 'path'

const provider = new Pact({
  consumer: 'elite-frontend',
  provider: 'elite-backend',
  port: 1234,
  log: path.resolve(process.cwd(), 'logs', 'pact.log'),
  dir: path.resolve(process.cwd(), 'pacts'),
  logLevel: 'warn',
})

describe('Auth API contract', () => {
  beforeAll(() => provider.setup())
  afterEach(() => provider.verify())
  afterAll(() => provider.finalize())

  it('returns a token for valid dev credentials', async () => {
    await provider.addInteraction({
      state: 'dev auth is enabled',
      uponReceiving: 'a request for a dev token',
      withRequest: {
        method: 'POST',
        path: '/api/v1/auth/token',
        headers: { 'Content-Type': 'application/json' },
        body: { email: 'test@example.com' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          access_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test',
          token_type: 'bearer',
        },
      },
    })

    const response = await fetch('http://localhost:1234/api/v1/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com' }),
    })

    expect(response.status).toBe(200)
    const data = await response.json()
    expect(data.token_type).toBe('bearer')
    expect(data.access_token).toBeDefined()
  })
})
