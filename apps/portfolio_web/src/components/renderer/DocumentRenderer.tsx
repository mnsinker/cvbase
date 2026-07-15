import { Prose } from '@/components/Prose'
import { TOC, type TocItem } from '@/components/TOC'

import { renderBlock, type DocNode, type Document } from './BlockRenderer'
import { isNodeVisible } from './visibility'

export type RenderOptions = {
  showAnnotations?: boolean
  headingIds?: Map<DocNode, string>
}

type DocumentRendererProps = {
  document: Document
  tocTitle?: string
  options?: RenderOptions
  showToc?: boolean
}

function getHeadingTitle(node: DocNode): string {
  return node.inline_children
    .filter((child) => child.type === 'Text')
    .map((child) => child.content)
    .join('')
    .trim()
}

function slugifyHeadingTitle(title: string): string {
  return title
    .normalize('NFKC')
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '')
}

function getUniqueHeadingId(slug: string, counts: Map<string, number>): string {
  const count = counts.get(slug) ?? 0
  const nextCount = count + 1

  counts.set(slug, nextCount)

  if (nextCount === 1) {
    return slug
  }

  return `${slug}-${nextCount}`
}

function buildTocItems(document: Document): {
  items: TocItem[]
  headingIds: Map<DocNode, string>
} {
  const items: TocItem[] = []
  const headingIds = new Map<DocNode, string>()
  const slugCounts = new Map<string, number>()

  function visit(node: DocNode) {
    if (!isNodeVisible(node)) {
      return
    }

    if (node.type === 'Heading' && (node.level === 1 || node.level === 2)) {
      const title = getHeadingTitle(node)
      const slug = slugifyHeadingTitle(title)

      if (title && slug) {
        const id = getUniqueHeadingId(slug, slugCounts)

        items.push({ id, title, level: node.level })
        headingIds.set(node, id)
      }
    }

    node.doc_children.forEach(visit)
  }

  document.doc_children.forEach(visit)

  return { items, headingIds }
}

export default function DocumentRenderer({
  document,
  tocTitle,
  options = {
    showAnnotations: false,
  },
  showToc = true,
}: DocumentRendererProps) {
  const { items, headingIds } = buildTocItems(document)
  const renderOptions = {
    ...options,
    headingIds,
  }

  return (
    <Prose>
      <div className={showToc ? 'flex gap-6' : undefined}>
        {showToc && items.length > 0 && (
          <TOC
            title={tocTitle}
            items={items}
          />
        )}

        <div className="min-w-0 flex-1">
          {document.doc_children.map((node, index) =>
            renderBlock(node, index, renderOptions),
          )}
        </div>
      </div>
    </Prose>
  )
}
