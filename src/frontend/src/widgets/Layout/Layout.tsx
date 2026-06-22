'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useAuthStore } from '@/features/auth/model/store'
import { Button } from '@/shared/ui'

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/time-tracker', label: 'Time tracker' },
  { href: '/invoices', label: 'Invoices' },
  { href: '/clients', label: 'Clients' },
  { href: '/projects', label: 'Projects' },
]

export function Layout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const { isAuthenticated, clearToken } = useAuthStore()

  const handleLogout = () => {
    clearToken()
    router.push('/login')
  }

  return (
    <div className="min-h-screen bg-elite-surface">
      <header className="border-b border-elite-border bg-elite-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <Link href="/" className="text-xl font-bold text-elite-text-primary">
            Elite
          </Link>
          {isAuthenticated && (
            <nav className="hidden items-center gap-1 md:flex">
              {navItems.map((item) => {
                const active = pathname === item.href
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    aria-current={active ? 'page' : undefined}
                    className={[
                      'rounded-md px-3 py-2 text-sm font-medium',
                      active
                        ? 'bg-elite-surface text-elite-text-primary'
                        : 'text-elite-text-secondary hover:bg-elite-surface hover:text-elite-text-primary',
                    ].join(' ')}
                  >
                    {item.label}
                  </Link>
                )
              })}
            </nav>
          )}
          {isAuthenticated ? (
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              Sign out
            </Button>
          ) : (
            <Link href="/login" className="text-sm font-medium text-elite-interactive hover:underline">
              Sign in
            </Link>
          )}
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  )
}
