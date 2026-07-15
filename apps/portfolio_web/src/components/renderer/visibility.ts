import type { DocNode } from './BlockRenderer'

export function isNodeVisible(node: DocNode): boolean {
  return !node.annotations.some(
    (annotation) =>
      annotation.key === 'excluded_visibility' &&
      annotation.values === true,
  )
}

export function showAnnotations(
  node: DocNode,
  enabled: boolean,
): boolean {
  return isNodeVisible(node) && enabled
}
