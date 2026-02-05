import { useEffect, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import Reveal from 'reveal.js'
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js'
import Highlight from 'reveal.js/plugin/highlight/highlight.esm.js'
import 'reveal.js/dist/reveal.css'
import 'reveal.js/dist/theme/black.css'
import 'reveal.js/plugin/highlight/monokai.css'
import { getSlide } from '@/utils'
import type { SlideData } from '@/types'

export function SlideViewer() {
  const { id } = useParams<{ id: string }>()
  const deckRef = useRef<HTMLDivElement>(null)
  const revealRef = useRef<Reveal.Api | null>(null)
  const [slide, setSlide] = useState<SlideData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // スライドデータを取得
  useEffect(() => {
    async function loadSlide() {
      if (!id) {
        setError('スライドIDが指定されていません')
        setIsLoading(false)
        return
      }

      try {
        const slideData = await getSlide(id)
        if (!slideData) {
          setError('スライドが見つかりませんでした')
        } else {
          setSlide(slideData)
        }
      } catch {
        setError('スライドの読み込みに失敗しました')
      } finally {
        setIsLoading(false)
      }
    }
    loadSlide()
  }, [id])

  // reveal.jsを初期化
  useEffect(() => {
    if (!slide || !deckRef.current) return

    const initReveal = async () => {
      // 既存のインスタンスを破棄
      if (revealRef.current) {
        revealRef.current.destroy()
      }

      const deck = new Reveal(deckRef.current!, {
        hash: false,
        history: false,
        controls: true,
        progress: true,
        center: true,
        transition: 'slide',
        width: 960,
        height: 700,
        margin: 0.1,
        minScale: 0.2,
        maxScale: 1.5,
        plugins: [Markdown, Highlight],
      })

      await deck.initialize()
      revealRef.current = deck
    }

    initReveal()

    return () => {
      if (revealRef.current) {
        revealRef.current.destroy()
        revealRef.current = null
      }
    }
  }, [slide])

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-200 border-t-primary-600 mx-auto" />
          <p className="text-gray-400">読み込み中...</p>
        </div>
      </div>
    )
  }

  if (error || !slide) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950">
        <div className="text-center">
          <h2 className="mb-4 text-2xl font-bold text-white">
            {error || 'エラーが発生しました'}
          </h2>
          <Link
            to="/"
            className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            一覧に戻る
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="relative min-h-screen">
      {/* 戻るボタン */}
      <Link
        to="/"
        className="fixed left-4 top-4 z-50 flex items-center gap-2 rounded-lg bg-gray-800/80 px-3 py-2 text-sm text-white backdrop-blur-sm transition-colors hover:bg-gray-700"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        一覧
      </Link>

      {/* reveal.js コンテナ */}
      <div className="reveal-container">
        <div ref={deckRef} className="reveal">
          <div className="slides">
            <section
              data-markdown=""
              data-separator="^---$"
              data-separator-vertical="^--$"
            >
              <script type="text/template">
                {slide.content}
              </script>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}
