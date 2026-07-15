import { notFound } from 'next/navigation'

import { articleLoaders } from '@/lib/articles'

type ArticlePageProps = {
  params: Promise<{
    locale: string
    slug: string
  }>
}

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { slug } = await params
  const loader = articleLoaders[slug as keyof typeof articleLoaders]
  if (!loader) {
    notFound()
  }

  const article = await loader()
  const Article = article.default
  return <Article />
}
