import { Fragment, type ReactNode } from 'react'
import Prism from 'prismjs'
import 'prismjs/components/prism-json'

import { renderInline, type InlineNode } from './InlineRenderer'
import { isNodeVisible, showAnnotations } from './visibility'
import type { RenderOptions } from '@/components/renderer/DocumentRenderer'

export type Annotation = {
  key: string
  values: boolean | string | string[]
}

export type DocNodeBase = {
  annotations: Annotation[]
  inline_children: InlineNode[]
  doc_children: DocNode[]

  view?: {
    visible: boolean
  }
}

export type DocNode =
  | Document
  | FrontMatter
  | Heading
  | Paragraph
  | ListItem
  | QuoteBlock
  | CodeBlock
  | MathBlock
  | HorizontalRule
  | Table
  | Row
  | Cell

export type Document = DocNodeBase & {
  type: 'Document'
}

export type FrontMatter = DocNodeBase & {
  type: 'FrontMatter'
  content: string[]
}

export type Heading = DocNodeBase & {
  type: 'Heading'
  level: number
}

export type Paragraph = DocNodeBase & {
  type: 'Paragraph'
}

export type ListItem = DocNodeBase & {
  type: 'ListItem'
  label: string
}

export type QuoteBlock = DocNodeBase & {
  type: 'QuoteBlock'
}

export type CodeBlock = DocNodeBase & {
  type: 'CodeBlock'
  language: string
  content: string[]
}

export type MathBlock = DocNodeBase & {
  type: 'MathBlock'
  content: string[]
}

export type HorizontalRule = DocNodeBase & {
  type: 'HorizontalRule'
}

export type Table = DocNodeBase & {
  type: 'Table'
}

export type Row = DocNodeBase & {
  type: 'Row'
}

export type Cell = DocNodeBase & {
  type: 'Cell'
}

function buildGroups(
  children: DocNode[],
): DocNode[][] {
  if (children.length === 0) {
    return []
  }

  if (children.length === 1) {
    return [children]
  }

  if (!children.some((child) => child.doc_children.length > 0)) {
    return [children]
  }

  const groups: DocNode[][] = []
  let leafGroup: DocNode[] = []

  children.forEach((child) => {
    if (child.doc_children.length > 0) {
      if (leafGroup.length > 0) {
        groups.push(leafGroup)
        leafGroup = []
      }

      groups.push([child])
      return
    }

    leafGroup.push(child)
  })

  if (leafGroup.length > 0) {
    groups.push(leafGroup)
  }

  return groups
}

function renderGroups(
  groups: DocNode[][],
  options: RenderOptions,
): ReactNode {
  return groups.map((group, groupIndex) => (
    <section key={groupIndex} className="group">
      <div className="group-items">
        {group.map((node, index) => renderBlock(node, index, options))}
      </div>
    </section>
  ))
}

function renderChildren(
  node: { doc_children: DocNode[] },
  options: RenderOptions,
): ReactNode {
  const visibleChildren = node.doc_children.filter(isNodeVisible)
  const groups = buildGroups(visibleChildren)

  return renderGroups(groups, options)
}

function renderInlineChildren(node: {
  inline_children: InlineNode[]
}): ReactNode {
  return node.inline_children.map((child, index) => (
    <Fragment key={index}>
      {renderInline(child, index)}
    </Fragment>
  ))
}

function renderAnnotations(
  node: DocNode,
  options: RenderOptions,
): ReactNode {
  if (!showAnnotations(node, options.showAnnotations ?? false)) {
    return null
  }

  return (
    <dl className="annotations">
      {node.annotations.map((annotation) => (
        <div key={annotation.key} className="annotation">
          <dt>{annotation.key}</dt>
          <dd>
            {Array.isArray(annotation.values)
              ? annotation.values.join(', ')
              : String(annotation.values)}
          </dd>
        </div>
      ))}
    </dl>
  )
}

export function renderBlock(
  node: DocNode,
  index: number,
  options: RenderOptions,
): ReactNode {
  if (!isNodeVisible(node)) {
    return null
  }

  switch (node.type) {
    case 'Document':
      return <>{renderChildren(node, options)}</>

    case 'FrontMatter':
      return null

    case 'Heading':
      switch (node.level) {
        case 1: {
          const headingId = options.headingIds?.get(node)

          return (
            <section key={index} id={headingId} className="doc-node">
              <h1>{renderInlineChildren(node)}</h1>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        }
        case 2: {
          const headingId = options.headingIds?.get(node)

          return (
            <section key={index} id={headingId} className="doc-node">
              <h2>{renderInlineChildren(node)}</h2>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        }
        case 3:
          return (
            <section key={index} className="doc-node">
              <h3>{renderInlineChildren(node)}</h3>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        case 4:
          return (
            <section key={index} className="doc-node">
              <h4>{renderInlineChildren(node)}</h4>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        case 5:
          return (
            <section key={index} className="doc-node">
              <h5>{renderInlineChildren(node)}</h5>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        case 6:
          return (
            <section key={index} className="doc-node">
              <h6>{renderInlineChildren(node)}</h6>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
        default:
          return (
            <section key={index} className="doc-node">
              <h1>{renderInlineChildren(node)}</h1>
              {renderAnnotations(node, options)}
              {renderChildren(node, options)}
            </section>
          )
      }

    case 'Paragraph':
      return (
        <section key={index} className="doc-node">
          <p>{renderInlineChildren(node)}</p>
          {renderAnnotations(node, options)}
          {renderChildren(node, options)}
        </section>
      )

    case 'ListItem':
      return (
        <li key={index} className="doc-node">
          {renderInlineChildren(node)}
          {renderAnnotations(node, options)}
          {renderChildren(node, options)}
        </li>
      )

    case 'QuoteBlock':
      return (
        <section key={index} className="doc-node">
          <blockquote>{renderChildren(node, options)}</blockquote>
          {renderAnnotations(node, options)}
        </section>
      )

    case 'CodeBlock': {
      const code = node.content.join('\n')
      const language = node.language?.toLowerCase() || 'text'

      if (language === 'json') {
        const highlightedCode = Prism.highlight(
          code,
          Prism.languages.json,
          'json',
        )

        return (
          <section key={index} className="doc-node">
            <pre className="language-json">
              <code
                className="language-json"
                dangerouslySetInnerHTML={{ __html: highlightedCode }}
              />
            </pre>
          </section>
        )
      }

      return (
        <section key={index} className="doc-node">
          <pre className={`language-${language}`}>
            <code className={`language-${language}`}>{code}</code>
          </pre>
        </section>
      )
    }

    case 'MathBlock':
      return (
        <section key={index} className="doc-node">
          <div>{node.content.join('\n')}</div>
        </section>
      )

    case 'HorizontalRule':
      return <hr key={index} />

    case 'Table':
      return <table key={index}>{renderChildren(node, options)}</table>

    case 'Row':
      return <tr key={index}>{renderChildren(node, options)}</tr>

    case 'Cell':
      return <td key={index}>{renderChildren(node, options)}</td>
  }
}
