/// <reference types="vite/client" />

declare module '*.md' {
  const content: string
  export default content
}

declare module 'reveal.js' {
  interface RevealOptions {
    hash?: boolean
    history?: boolean
    controls?: boolean
    progress?: boolean
    center?: boolean
    transition?: string
    width?: number
    height?: number
    margin?: number
    minScale?: number
    maxScale?: number
    plugins?: unknown[]
  }

  interface RevealApi {
    initialize(): Promise<void>
    destroy(): void
    slide(h: number, v?: number, f?: number): void
  }

  class Reveal {
    constructor(element: HTMLElement, options?: RevealOptions)
    initialize(): Promise<void>
    destroy(): void
    slide(h: number, v?: number, f?: number): void
  }

  namespace Reveal {
    export type Api = RevealApi
  }

  export default Reveal
}

declare module 'reveal.js/plugin/markdown/markdown.esm.js' {
  const plugin: () => unknown
  export default plugin
}

declare module 'reveal.js/plugin/highlight/highlight.esm.js' {
  const plugin: () => unknown
  export default plugin
}
