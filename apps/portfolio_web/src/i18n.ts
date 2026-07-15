export const locales = ['en', 'zh'] as const

export type Locale = (typeof locales)[number]
export type I18n = Locale

export const defaultLocale: Locale = 'en'

export function isLocale(value: string): value is Locale {
  return locales.includes(value as Locale)
}

export function localizePath(pathname: string, locale: Locale): string {
  const normalizedPath =
    pathname === '/' ? '' : pathname.startsWith('/') ? pathname : `/${pathname}`

  return `/${locale}${normalizedPath}`
}

export function switchLocalePath(pathname: string, locale: Locale): string {
  const segments = pathname.split('/')

  if (segments[1] && isLocale(segments[1])) {
    segments[1] = locale
    return segments.join('/') || `/${locale}`
  }

  return localizePath(pathname, locale)
}
