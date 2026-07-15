import type { ReactNode } from 'react'
import Link from 'next/link'
import React from 'react'

export type InlineNodeBase = {
  inline_children: InlineNode[]
}

export type InlineNode =
  | Text
  | Strong
  | Italic
  | Strike
  | Underline
  | InlineMath
  | InlineCode
  | LinkNode
  | Image

export type Text = InlineNodeBase & {
  type: 'Text'
  content: string
}

export type Strong = InlineNodeBase & {
  type: 'Strong'
}

export type Italic = InlineNodeBase & {
  type: 'Italic'
}

export type Strike = InlineNodeBase & {
  type: 'Strike'
}

export type Underline = InlineNodeBase & {
  type: 'Underline'
}

export type InlineMath = InlineNodeBase & {
  type: 'InlineMath'
}

export type InlineCode = InlineNodeBase & {
  type: 'InlineCode'
}

export type LinkNode = InlineNodeBase & {
  type: 'Link'
  url: string
  title?: string
}

export type Image = InlineNodeBase & {
  type: 'Image'
  src: string
  title?: string
}

function renderInlineChildren(node: {
  inline_children: InlineNode[]
}): ReactNode {
  return node.inline_children.map((child, index) => (
    <React.Fragment key={index}>
      {renderInline(child, index)}
    </React.Fragment>
  ))
}

export function renderInline(node: InlineNode, index: number): ReactNode {
  switch (node.type) {
    case 'Text':
      return <>{node.content}</>

    case 'Strong':
      return <strong key={index}>{renderInlineChildren(node)}</strong>

    case 'Italic':
      return <em key={index}>{renderInlineChildren(node)}</em>

    case 'Strike':
      return <s key={index}>{renderInlineChildren(node)}</s>

    case 'Underline':
      return <u key={index}>{renderInlineChildren(node)}</u>

    case 'InlineMath':
      return <span key={index}>{renderInlineChildren(node)}</span>

    case 'InlineCode':
      return <code key={index}>{renderInlineChildren(node)}</code>

    case 'Link':
      return (
        <Link key={index} href={node.url} title={node.title || undefined}>
          {renderInlineChildren(node)}
        </Link>
      )

    case 'Image':
      return (
        <img
          key={index}
          src={node.src}
          title={node.title || undefined}
          alt={node.title}
        />
      )
  }
}
