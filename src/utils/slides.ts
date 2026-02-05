import type { SlideMetadata, SlideData } from '@/types'

// スライドモジュールをViteのglobでインポート
const slideModules = import.meta.glob<string>('/slides/**/slide.md', {
  query: '?raw',
  import: 'default',
})

// フロントマターをパース（簡易実装）
function parseFrontmatter(content: string): { data: Record<string, unknown>; content: string } {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/
  const match = content.match(frontmatterRegex)

  if (!match) {
    return { data: {}, content }
  }

  const yamlContent = match[1]
  const markdownContent = match[2]

  // 簡易YAMLパーサー
  const data: Record<string, unknown> = {}
  let currentKey = ''
  let inArray = false
  let arrayItems: string[] = []

  yamlContent.split('\n').forEach((line) => {
    const trimmed = line.trim()

    if (inArray) {
      if (trimmed.startsWith('- ')) {
        arrayItems.push(trimmed.slice(2).trim())
      } else if (trimmed && !trimmed.startsWith('-')) {
        data[currentKey] = arrayItems
        arrayItems = []
        inArray = false
      }
    }

    if (!inArray) {
      const colonIndex = line.indexOf(':')
      if (colonIndex > 0) {
        const key = line.slice(0, colonIndex).trim()
        const value = line.slice(colonIndex + 1).trim()

        if (value === '') {
          currentKey = key
          inArray = true
          arrayItems = []
        } else {
          data[key] = value.replace(/^["']|["']$/g, '')
        }
      }
    }
  })

  if (inArray && arrayItems.length > 0) {
    data[currentKey] = arrayItems
  }

  return { data, content: markdownContent }
}

// IDをパスから抽出
function extractIdFromPath(path: string): string {
  const match = path.match(/\/slides\/([^/]+)\/slide\.md$/)
  return match ? match[1] : ''
}

// すべてのスライドメタデータを取得
export async function getAllSlides(): Promise<SlideMetadata[]> {
  const slides: SlideMetadata[] = []

  for (const [path, loader] of Object.entries(slideModules)) {
    const content = await loader()
    const { data } = parseFrontmatter(content)
    const id = extractIdFromPath(path)

    slides.push({
      id,
      title: (data.title as string) || 'Untitled',
      date: (data.date as string) || '',
      description: (data.description as string) || '',
      tags: (data.tags as string[]) || [],
      author: data.author as string | undefined,
    })
  }

  // 日付で降順ソート
  return slides.sort((a, b) => b.date.localeCompare(a.date))
}

// 特定のスライドを取得
export async function getSlide(id: string): Promise<SlideData | null> {
  const path = `/slides/${id}/slide.md`

  if (!slideModules[path]) {
    return null
  }

  const content = await slideModules[path]()
  const { data, content: markdownContent } = parseFrontmatter(content)

  return {
    id,
    title: (data.title as string) || 'Untitled',
    date: (data.date as string) || '',
    description: (data.description as string) || '',
    tags: (data.tags as string[]) || [],
    author: data.author as string | undefined,
    content: markdownContent,
  }
}

// すべてのタグを取得
export async function getAllTags(): Promise<string[]> {
  const slides = await getAllSlides()
  const tagSet = new Set<string>()

  slides.forEach((slide) => {
    slide.tags.forEach((tag) => tagSet.add(tag))
  })

  return Array.from(tagSet).sort()
}
