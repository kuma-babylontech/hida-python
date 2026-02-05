import { Link } from 'react-router-dom'
import { ThemeToggle } from '../common/ThemeToggle'

const LOGO_URL = 'https://media.connpass.com/thumbs/70/c3/70c3b27a9aa717bbd26062e6da529a10.png'

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-sm dark:border-gray-800 dark:bg-gray-950/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3">
          <img
            src={LOGO_URL}
            alt="飛騨高山Pythonの会"
            className="h-10 w-10 rounded-lg"
          />
          <h1 className="text-lg font-bold text-gray-900 dark:text-white">
            飛騨高山Pythonの会スライド
          </h1>
        </Link>
        <ThemeToggle />
      </div>
    </header>
  )
}
