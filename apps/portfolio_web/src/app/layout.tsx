import { type Metadata } from 'next'

import { Providers } from '@/app/providers'
import { Layout } from '@/components/Layout'

import '@/styles/tailwind.css'

export const metadata: Metadata = {
  metadataBase: new URL('https://mnsink-portfolio.vercel.app'),
  title: {
    template: '%s | Jieni Zhang',
    default: 'Jieni Zhang | Applied AI Engineer',
  },
  description:
    'Applied AI Engineer building systems that turn knowledge into decisions, actions, and continuous learning.',
  openGraph: {
    title: 'Jieni Zhang | Applied AI Engineer',
    description:
      'Applied AI Engineer building systems that turn knowledge into decisions, actions, and continuous learning.',
    url: '/',
    siteName: 'Jieni Zhang',
    type: 'website',
  },
  alternates: {
    types: {
      'application/rss+xml': '/feed.xml',
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full antialiased" suppressHydrationWarning>
      <body className="flex h-full bg-zinc-50 dark:bg-black">
        <Providers>
          <div className="flex w-full">
            <Layout>{children}</Layout>
          </div>
        </Providers>
      </body>
    </html>
  )
}
