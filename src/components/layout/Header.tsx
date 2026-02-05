import { Link } from 'react-router-dom'
import { ThemeToggle } from '../common/ThemeToggle'

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-sm dark:border-gray-800 dark:bg-gray-950/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-[#306998] to-[#4B8BBE]">
            <span className="text-lg font-bold text-[#FFD43B]">Py</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">
              hida-python
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              飛騨高山Pythonの会スライド
            </p>
          </div>
        </Link>
        <ThemeToggle />
      </div>
    </header>
  )
}
