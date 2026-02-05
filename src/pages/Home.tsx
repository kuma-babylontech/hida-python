import { useState, useEffect, useMemo } from 'react'
import { SlideListItem, TagFilter } from '@/components/slides'
import { getAllSlides, getAllTags } from '@/utils'
import type { SlideMetadata } from '@/types'

export function Home() {
  const [slides, setSlides] = useState<SlideMetadata[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [slidesData, tagsData] = await Promise.all([
          getAllSlides(),
          getAllTags(),
        ])
        setSlides(slidesData)
        setTags(tagsData)
      } finally {
        setIsLoading(false)
      }
    }
    loadData()
  }, [])

  const filteredSlides = useMemo(() => {
    if (selectedTags.length === 0) return slides
    return slides.filter((slide) =>
      selectedTags.every((tag) => slide.tags.includes(tag))
    )
  }, [slides, selectedTags])

  const handleTagToggle = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    )
  }

  const handleClearTags = () => {
    setSelectedTags([])
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-200 border-t-primary-600 mx-auto" />
          <p className="text-gray-600 dark:text-gray-400">読み込み中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* ヘッダー */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">
          スライド一覧
        </h2>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          飛騨高山Pythonの会で発表したスライド資料
        </p>
      </div>

      {/* タグフィルター */}
      <TagFilter
        tags={tags}
        selectedTags={selectedTags}
        onTagToggle={handleTagToggle}
        onClearAll={handleClearTags}
      />

      {/* スライド一覧 */}
      {filteredSlides.length > 0 ? (
        <div className="flex flex-col gap-3">
          {filteredSlides.map((slide) => (
            <SlideListItem key={slide.id} slide={slide} />
          ))}
        </div>
      ) : (
        <div className="rounded-lg border-2 border-dashed border-gray-200 p-12 text-center dark:border-gray-800">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
            <svg
              className="h-8 w-8 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
            スライドがありません
          </h3>
          <p className="text-gray-500 dark:text-gray-400">
            {selectedTags.length > 0
              ? '選択したタグに一致するスライドがありません'
              : 'slides/ ディレクトリにスライドを追加してください'}
          </p>
        </div>
      )}
    </div>
  )
}
