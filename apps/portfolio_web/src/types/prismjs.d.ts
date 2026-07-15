declare module 'prismjs' {
  type Grammar = Record<string, unknown>
  const Prism: {
    languages: {
      json: Grammar
    }
    highlight(
      code: string,
      grammar: Grammar,
      language: string,
    ): string
  }
  export default Prism
}

declare module 'prismjs/components/prism-json'
