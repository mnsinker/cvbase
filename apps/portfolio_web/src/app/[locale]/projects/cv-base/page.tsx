import path from 'node:path'

import { Container } from '@/components/Container'
import JsonDocumentRenderer from '@/components/renderer/JsonDocumentRenderer'
import { isLocale, type Locale } from '@/i18n'
import { notFound } from 'next/navigation'

type CVBasePageProps = { params: Promise<{ locale: string }> }

export default async function CVBasePage({ params }: CVBasePageProps) {
  const { locale: rawLocale } = await params
  if (!isLocale(rawLocale)) notFound()
  const locale: Locale = rawLocale
  const jsonPath = path.join(
    process.cwd(),
    'content/projects/cv-base',
    `${locale}.json`,
  )
  return (
    <Container className="mt-16 sm:mt-32">
      <section className="mb-16">
        <h1 className="mb-6 text-3xl font-bold text-zinc-100">
          Project Walkthrough
        </h1>

        <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950">
          <video
            controls
            preload="metadata"
            className="block aspect-video w-full"
          >
            <source
              src=""
              type="video/mp4"
            />
            Your browser does not support video playback.
          </video>
        </div>
      </section>

      <JsonDocumentRenderer jsonPath={jsonPath} />
    </Container>
  )}

//   return (
//     <Container className="mt-16 sm:mt-32">
//       <JsonDocumentRenderer jsonPath={jsonPath} />
//     </Container>
//   )
// }
