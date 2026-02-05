import { Link } from 'react-router-dom'
import type { SlideMetadata } from '@/types'

interface SlideCardProps {
  slide: SlideMetadata
}

export function SlideCard({ slide }: SlideCardProps) {
  const formatDate = (dateString: string) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  return (
    <Link
      to={`/slides/${slide.id}`}
      className="group block overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all hover:shadow-lg dark:border-gray-800 dark:bg-gray-900"
    >
      {/* サムネイル */}
      <div className="aspect-video overflow-hidden bg-gradient-to-br from-[#306998] to-[#4B8BBE]">
        <img
          src={slide.thumbnail}
          alt={`${slide.title}のサムネイル`}
          className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
          onError={(e) => {
            const target = e.target as HTMLImageElement
            target.style.display = 'none'
          }}
        />
        <div className="flex h-full items-center justify-center">
          <span className="text-4xl font-bold text-[#FFD43B]">Py</span>
        </div>
      </div>

      {/* コンテンツ */}
      <div className="p-4">
        <h3 className="mb-2 text-lg font-semibold text-gray-900 group-hover:text-primary-600 dark:text-white dark:group-hover:text-primary-400">
          {slide.title}
        </h3>

        <p className="mb-3 line-clamp-2 text-sm text-gray-600 dark:text-gray-400">
          {slide.description}
        </p>

        {/* タグ */}
        <div className="mb-3 flex flex-wrap gap-1">
          {slide.tags.map((tag) => (
            <span
              key={tag}
              className="inline-block rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* メタ情報 */}
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-500">
          <time dateTime={slide.date}>{formatDate(slide.date)}</time>
          {slide.author && <span>{slide.author}</span>}
        </div>
      </div>
    </Link>
  )
}
