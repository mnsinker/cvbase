'use client'

import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from 'react'

type Locale = 'en' | 'zh'

type LocaleContextType = {
  locale: Locale
  setLocale: (next: Locale) => void
}

const LocaleContext = createContext<LocaleContextType | null>(null)

export function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>('en')

  return (
    <LocaleContext.Provider value={{ locale, setLocale }}>
      {children}
    </LocaleContext.Provider>
  )
}

export function useLocale(): LocaleContextType {
  let ctx = useContext(LocaleContext)
  if (!ctx) {
    throw new Error('useLocale must be used within a <LocaleProvider>')
  }
  return ctx
}
