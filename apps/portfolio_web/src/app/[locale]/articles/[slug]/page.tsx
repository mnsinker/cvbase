import { notFound } from 'next/navigation'

type ArticlePageProps = {
  params: Promise<{
    locale: string
    slug: string
  }>
}

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { slug } = await params
  let article

  try {
    article = await import(`../../../../content/articles/${slug}/page.mdx`)
  } catch {
    notFound()
  }

  const Article = article.default
  return <Article />
}
