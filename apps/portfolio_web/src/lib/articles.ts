interface Article {
  title: string
  description: string
  author: string
  date: string
}

export interface ArticleWithSlug extends Article {
  slug: string
}

export const articleLoaders = {
  'crafting-a-design-system-for-a-multiplanetary-future': () =>
    import(
      '../../content/articles/crafting-a-design-system-for-a-multiplanetary-future/page.mdx'
    ),
  'introducing-animaginary': () =>
    import('../../content/articles/introducing-animaginary/page.mdx'),
  'rewriting-the-cosmos-kernel-in-rust': () =>
    import('../../content/articles/rewriting-the-cosmos-kernel-in-rust/page.mdx'),
} as const

async function importArticle(
  slug: keyof typeof articleLoaders,
): Promise<ArticleWithSlug> {
  const articleModule = (await articleLoaders[slug]()) as {
    default: React.ComponentType
    article: Article
  }
  const { article } = articleModule

  return { slug, ...article }
}

export async function getAllArticles() {
  const articles = await Promise.all(
    Object.keys(articleLoaders).map((slug) =>
      importArticle(slug as keyof typeof articleLoaders),
    ),
  )

  return articles.sort((a, z) => +new Date(z.date) - +new Date(a.date))
}
