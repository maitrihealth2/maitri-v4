import type { Metadata } from 'next'
import { Literata } from 'next/font/google'
import { Providers } from './providers'
import './globals.css'

const literata = Literata({
  subsets: ['latin'],
  variable: '--font-literata',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Mythri | Sanctuary',
  description: 'A safe, quiet space for reflection and healing.',
  keywords: 'mental health, AI companion, therapy, support',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="light bg-immersive" suppressHydrationWarning>
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
      </head>
      <body className={`${literata.variable} font-body-md antialiased bg-immersive h-[100dvh] flex flex-col text-on-background relative md:overflow-hidden`}>
        {/* Background Grain and Ambient Blobs */}
        <div className="bg-grain"></div>
        {/* Desktop Blobs (hidden on small) */}
        <div className="hidden md:block fixed top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-tertiary-fixed/30 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
        <div className="hidden md:block fixed bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-secondary-fixed/40 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
        {/* Mobile Blobs (hidden on md) */}
        <div className="block md:hidden fixed top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-slate-300/40 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
        <div className="block md:hidden fixed bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-stone-200/50 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
        
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}

