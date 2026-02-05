export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-gray-200 bg-white py-6 dark:border-gray-800 dark:bg-gray-950">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-gray-500 dark:text-gray-400">
          © {currentYear} Babylon Tech Inc.
        </p>
      </div>
    </footer>
  )
}
