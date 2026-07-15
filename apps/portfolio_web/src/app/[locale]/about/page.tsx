import { notFound, redirect } from 'next/navigation'
import { isLocale } from '@/i18n'

type AboutPageProps = {
  params: Promise<{ locale: string }>
}

export default async function AboutPage({ params }: AboutPageProps) {
  const { locale } = await params
  if (!isLocale(locale)) {
    notFound()
  }
  redirect(`/${locale}`)
}
