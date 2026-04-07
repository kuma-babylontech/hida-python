interface TagFilterProps {
  tags: string[]
  selectedTags: string[]
  onTagToggle: (tag: string) => void
  onClearAll: () => void
}

export function TagFilter({ tags, selectedTags, onTagToggle, onClearAll }: TagFilterProps) {
  if (tags.length === 0) return null

  return (
    <div className="mb-6 flex flex-wrap items-center gap-2 py-4 border-b border-white/5">
      <span
        className="text-[10px] tracking-[0.2em] uppercase text-gray-600 mr-2"
        style={{ fontFamily: 'var(--font-mono)' }}
      >
        filter
      </span>
      {tags.map((tag) => {
        const isSelected = selectedTags.includes(tag)
        return (
          <button
            key={tag}
            onClick={() => onTagToggle(tag)}
            className={`tag-pill rounded-sm px-2.5 py-1 cursor-pointer ${isSelected ? 'active' : ''}`}
          >
            {tag}
          </button>
        )
      })}
      {selectedTags.length > 0 && (
        <button
          onClick={onClearAll}
          className="text-[10px] tracking-wider text-gray-600 hover:text-gray-400 transition-colors ml-2 cursor-pointer"
          style={{ fontFamily: 'var(--font-mono)' }}
        >
          clear
        </button>
      )}
    </div>
  )
}
