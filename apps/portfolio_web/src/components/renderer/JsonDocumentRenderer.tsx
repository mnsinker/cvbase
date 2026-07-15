import fs from 'node:fs'
import path from 'node:path'

import DocumentRenderer, { type RenderOptions } from './DocumentRenderer'
import type { Document } from './BlockRenderer'

type JsonDocumentRendererProps = {
  jsonPath: string
  options?: RenderOptions
  showToc?: boolean
}

export default function JsonDocumentRenderer({
  jsonPath,
  options,
  showToc,
}: JsonDocumentRendererProps) {
  const rawJson = fs.readFileSync(jsonPath, 'utf-8')
  const documentJson = JSON.parse(rawJson) as Document
  const parentFolderName = path.basename(path.dirname(jsonPath))
  const tocTitle = parentFolderName
    .split('-')
    .map((word) => {
      const upper = word.toUpperCase()
      if (upper === 'CV' || upper === 'AI') {
        return upper
      }
      return word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join(' ')

  return (
    <DocumentRenderer
      document={documentJson}
      tocTitle={tocTitle}
      options={options}
      showToc={showToc}
    />
  )
}
