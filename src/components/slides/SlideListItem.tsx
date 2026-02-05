import { Link } from 'react-router-dom'
import type { SlideMetadata } from '@/types'

interface SlideListItemProps {
  slide: SlideMetadata
}

export function SlideListItem({ slide }: SlideListItemProps) {
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
      className="group block rounded-lg border border-gray-200 bg-white p-4 transition-all hover:border-primary-300 hover:shadow-md dark:border-gray-800 dark:bg-gray-900 dark:hover:border-primary-700"
    >
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 dark:text-white dark:group-hover:text-primary-400">
            {slide.title}
          </h3>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            {slide.description}
          </p>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {slide.tags.map((tag) => (
              <span
                key={tag}
                className="inline-block rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-500 sm:flex-col sm:items-end sm:gap-1">
          <time dateTime={slide.date}>{formatDate(slide.date)}</time>
          {slide.author && <span>{slide.author}</span>}
        </div>
      </div>
    </Link>
  )
}
