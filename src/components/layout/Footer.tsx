export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-white/5 py-8 mt-auto">
      <div className="mx-auto max-w-6xl px-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="accent-dot" />
            <a
              href="https://hida-python.connpass.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs tracking-wider text-gray-500 hover:text-hida-cedar-light transition-colors"
              style={{ fontFamily: 'var(--font-mono)' }}
            >
              hida-python.connpass.com
            </a>
          </div>
          <p className="text-xs text-gray-600" style={{ fontFamily: 'var(--font-mono)' }}>
            &copy; {currentYear} Babylon Tech Inc.
          </p>
        </div>
      </div>
    </footer>
  )
}
