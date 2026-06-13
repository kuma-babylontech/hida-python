import { Link } from 'react-router-dom'

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/5 bg-hida-ink/80 backdrop-blur-xl">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="flex items-center gap-2">
            <span className="text-python-yellow text-lg font-bold" style={{ fontFamily: 'var(--font-mono)' }}>
              &gt;_
            </span>
            <span className="text-sm font-medium tracking-wide text-gray-400 group-hover:text-gray-200 transition-colors">
              飛騨高山<span className="text-python-blue">Python</span>の会
            </span>
          </div>
        </Link>
      </div>
    </header>
  )
}
