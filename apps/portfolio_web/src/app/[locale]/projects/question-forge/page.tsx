import path from 'node:path'

import { Container } from '@/components/Container'
import JsonDocumentRenderer from '@/components/renderer/JsonDocumentRenderer'
import { isLocale, type Locale } from '@/i18n'
import { notFound } from 'next/navigation'

type QuestionForgePageProps = { params: Promise<{ locale: string }> }

export default async function QuestionForgePage({ params }: QuestionForgePageProps) {
  const { locale: rawLocale } = await params
  if (!isLocale(rawLocale)) notFound()
  const locale: Locale = rawLocale
  const jsonPath = path.join(
    process.cwd(),
    'content/projects/question-forge',
    `${locale}.json`,
  )
  return (
    <Container className="mt-16 sm:mt-32">
      <JsonDocumentRenderer jsonPath={jsonPath} />
    </Container>
  )
}
