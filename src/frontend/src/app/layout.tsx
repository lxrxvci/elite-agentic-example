import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { QueryProvider } from './providers'
import { ToastProvider } from '@/shared/ui'
import { Layout } from '@/widgets/Layout/Layout'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'Elite — Freelancer Dashboard',
  description: 'Track time, invoice clients, and get paid faster.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans`}>
        <QueryProvider>
          <ToastProvider>
            <Layout>{children}</Layout>
          </ToastProvider>
        </QueryProvider>
      </body>
    </html>
  )
}
