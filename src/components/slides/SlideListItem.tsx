import { Link } from 'react-router-dom'
import type { SlideMetadata } from '@/types'

interface SlideListItemProps {
  slide: SlideMetadata
}

export function SlideListItem({ slide }: SlideListItemProps) {
  const formatDate = (dateString: string) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    return `${year}.${month}`
  }

  return (
    <Link
      to={`/slides/${slide.id}`}
      className="slide-card group block rounded-sm px-5 py-5 sm:px-6"
    >
      <div className="flex flex-col sm:flex-row sm:items-start gap-4">
        {/* Date column */}
        <div className="sm:w-20 shrink-0">
          <time
            dateTime={slide.date}
            className="text-xs tracking-widest text-gray-600 tabular-nums"
            style={{ fontFamily: 'var(--font-mono)' }}
          >
            {formatDate(slide.date)}
          </time>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className="text-base sm:text-lg font-semibold text-gray-200 group-hover:text-python-yellow transition-colors duration-300 leading-snug"
            style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }}
          >
            {slide.title}
          </h3>
          <p className="mt-1.5 text-sm text-gray-500 leading-relaxed line-clamp-2">
            {slide.description}
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {slide.tags.map((tag) => (
              <span
                key={tag}
                className="tag-pill rounded-sm px-2 py-0.5"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>

        {/* Arrow */}
        <div className="hidden sm:flex items-center self-center">
          <svg
            className="h-4 w-4 text-gray-700 group-hover:text-hida-cedar-light group-hover:translate-x-1 transition-all duration-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </Link>
  )
}
