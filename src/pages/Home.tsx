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
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="relative h-10 w-10">
            <div className="absolute inset-0 rounded-full border border-python-yellow/30 animate-ping" />
            <div className="absolute inset-2 rounded-full border border-python-blue/50 animate-pulse" />
            <div className="absolute inset-[14px] accent-dot" />
          </div>
          <p className="text-xs tracking-widest text-gray-600 uppercase" style={{ fontFamily: 'var(--font-mono)' }}>
            loading
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-6xl px-6">
      {/* Hero */}
      <div className="hero-gradient pt-16 pb-12 sm:pt-24 sm:pb-16">
        <div className="animate-slide-up">
          <p
            className="text-xs tracking-[0.3em] uppercase text-hida-cedar-light mb-4"
            style={{ fontFamily: 'var(--font-mono)' }}
          >
            Hida Takayama Python Meetup
          </p>
          <h1
            className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-100 leading-tight"
            style={{ fontFamily: 'var(--font-display)', fontWeight: 800 }}
          >
            飛騨高山
            <br />
            <span className="text-python-blue">Python</span>
            <span className="text-gray-500">の会</span>
          </h1>
        </div>

        <div className="animate-slide-up mt-6" style={{ animationDelay: '0.1s' }}>
          <div className="animate-draw-line section-line max-w-xs" style={{ animationDelay: '0.4s' }} />
        </div>

        <div className="animate-slide-up mt-6 max-w-lg" style={{ animationDelay: '0.2s' }}>
          <p className="text-sm leading-relaxed text-gray-500">
            勉強会で発表したスライド資料のアーカイブ。
            <br className="hidden sm:block" />
            Pythonを中心に、Web開発・データ分析・AI活用まで。
          </p>
        </div>

        <div className="animate-slide-up mt-8 flex items-center gap-4" style={{ animationDelay: '0.3s' }}>
          <a
            href="https://hida-python.connpass.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-python-yellow/30 bg-python-yellow/5 px-5 py-2.5 text-xs font-medium tracking-wider text-python-yellow hover:bg-python-yellow/10 hover:border-python-yellow/50 transition-all"
            style={{ fontFamily: 'var(--font-mono)' }}
          >
            <span className="accent-dot" style={{ width: 4, height: 4 }} />
            Connpass
          </a>
          <span className="text-gray-700 text-xs" style={{ fontFamily: 'var(--font-mono)' }}>
            {slides.length} slides
          </span>
        </div>
      </div>

      {/* Filter + List */}
      <div className="pb-16">
        <div className="animate-slide-up" style={{ animationDelay: '0.35s' }}>
          <TagFilter
            tags={tags}
            selectedTags={selectedTags}
            onTagToggle={handleTagToggle}
            onClearAll={handleClearTags}
          />
        </div>

        {filteredSlides.length > 0 ? (
          <div className="flex flex-col gap-1">
            {filteredSlides.map((slide, index) => (
              <div
                key={slide.id}
                className="animate-slide-up"
                style={{ animationDelay: `${0.4 + index * 0.08}s` }}
              >
                <SlideListItem slide={slide} />
              </div>
            ))}
          </div>
        ) : (
          <div className="animate-fade-in mt-12 text-center py-16">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full border border-white/10 mb-4">
              <svg
                className="h-5 w-5 text-gray-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <p className="text-sm text-gray-600">
              {selectedTags.length > 0
                ? '一致するスライドがありません'
                : 'スライドがまだありません'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
