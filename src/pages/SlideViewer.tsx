import { useEffect, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import Reveal from 'reveal.js'
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js'
import Highlight from 'reveal.js/plugin/highlight/highlight.esm.js'
import 'reveal.js/dist/reveal.css'
import '@/styles/reveal-hida.css'
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
  const [backVisible, setBackVisible] = useState(true)
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

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

  // 戻るボタンの自動非表示
  useEffect(() => {
    const resetTimer = () => {
      setBackVisible(true)
      if (hideTimer.current) clearTimeout(hideTimer.current)
      hideTimer.current = setTimeout(() => setBackVisible(false), 3000)
    }

    resetTimer()
    window.addEventListener('mousemove', resetTimer)
    window.addEventListener('touchstart', resetTimer)

    return () => {
      window.removeEventListener('mousemove', resetTimer)
      window.removeEventListener('touchstart', resetTimer)
      if (hideTimer.current) clearTimeout(hideTimer.current)
    }
  }, [])

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center" style={{ background: '#0c0c12' }}>
        <div className="flex flex-col items-center gap-4">
          <div className="relative h-10 w-10">
            <div className="absolute inset-0 rounded-full border border-python-yellow/30 animate-ping" />
            <div className="absolute inset-2 rounded-full border border-python-blue/50 animate-pulse" />
            <div className="absolute inset-[14px] accent-dot" />
          </div>
          <p
            className="text-[10px] tracking-[0.3em] uppercase"
            style={{ fontFamily: 'var(--font-mono)', color: 'rgba(196,163,90,0.4)' }}
          >
            loading
          </p>
        </div>
      </div>
    )
  }

  if (error || !slide) {
    return (
      <div className="flex min-h-screen items-center justify-center kumiko-bg" style={{ background: '#0c0c12' }}>
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full border border-white/10 mb-6">
            <svg
              className="h-7 w-7"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              style={{ color: 'rgba(196,163,90,0.5)' }}
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <p
            className="mb-8 text-sm"
            style={{ color: 'rgba(212,207,196,0.6)' }}
          >
            {error || 'エラーが発生しました'}
          </p>
          <Link
            to="/"
            className="inline-flex items-center gap-2 rounded-sm border px-5 py-2.5 text-xs tracking-wider transition-all"
            style={{
              fontFamily: 'var(--font-mono)',
              borderColor: 'rgba(196,163,90,0.2)',
              color: '#C4A35A',
            }}
          >
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            BACK
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="relative min-h-screen">
      {/* 戻るボタン — マウス静止で自動非表示 */}
      <Link
        to="/"
        className="fixed left-4 top-4 z-50 flex items-center gap-2 rounded-sm px-3 py-2 text-[10px] tracking-[0.15em] uppercase transition-all duration-500"
        style={{
          fontFamily: 'var(--font-mono)',
          background: 'rgba(10, 10, 15, 0.7)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(196, 163, 90, 0.12)',
          color: 'rgba(196, 163, 90, 0.6)',
          opacity: backVisible ? 1 : 0,
          pointerEvents: backVisible ? 'auto' : 'none',
          transform: backVisible ? 'translateY(0)' : 'translateY(-8px)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = 'rgba(196, 163, 90, 0.35)'
          e.currentTarget.style.color = '#C4A35A'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = 'rgba(196, 163, 90, 0.12)'
          e.currentTarget.style.color = 'rgba(196, 163, 90, 0.6)'
        }}
      >
        <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        back
      </Link>

      {/* スライドメタ情報 — 左下 */}
      <div
        className="fixed left-4 bottom-4 z-50 max-w-xs transition-all duration-500"
        style={{
          opacity: backVisible ? 1 : 0,
          transform: backVisible ? 'translateY(0)' : 'translateY(8px)',
          pointerEvents: 'none',
        }}
      >
        <p
          className="text-[10px] tracking-wider truncate"
          style={{
            fontFamily: 'var(--font-mono)',
            color: 'rgba(196, 163, 90, 0.3)',
          }}
        >
          {slide.title}
        </p>
      </div>

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
