import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { SlideCard } from '@/components/slides/SlideCard'
import type { SlideMetadata } from '@/types'

const mockSlide: SlideMetadata = {
  id: '2025-01-python-basics',
  title: 'Pythonの基礎',
  date: '2025-01-15',
  description: 'Python入門者向けの基礎文法解説',
  tags: ['基礎', '入門'],
  author: 'hida-python',
  thumbnail: '/thumbnails/2025-01-python-basics.png',
}

describe('SlideCard', () => {
  it('should render slide title', () => {
    render(
      <BrowserRouter>
        <SlideCard slide={mockSlide} />
      </BrowserRouter>
    )

    expect(screen.getByText('Pythonの基礎')).toBeInTheDocument()
  })

  it('should render slide description', () => {
    render(
      <BrowserRouter>
        <SlideCard slide={mockSlide} />
      </BrowserRouter>
    )

    expect(screen.getByText('Python入門者向けの基礎文法解説')).toBeInTheDocument()
  })

  it('should render all tags', () => {
    render(
      <BrowserRouter>
        <SlideCard slide={mockSlide} />
      </BrowserRouter>
    )

    expect(screen.getByText('基礎')).toBeInTheDocument()
    expect(screen.getByText('入門')).toBeInTheDocument()
  })

  it('should link to slide detail page', () => {
    render(
      <BrowserRouter>
        <SlideCard slide={mockSlide} />
      </BrowserRouter>
    )

    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', '/slides/2025-01-python-basics')
  })

  it('should display formatted date', () => {
    render(
      <BrowserRouter>
        <SlideCard slide={mockSlide} />
      </BrowserRouter>
    )

    // 日本語フォーマットの日付を確認
    expect(screen.getByText(/2025年1月15日/)).toBeInTheDocument()
  })
})
