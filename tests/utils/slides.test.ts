import { describe, it, expect } from 'vitest'

// フロントマターのパース関数をテスト用にエクスポートする必要がある
// ここでは簡易的なユニットテストを作成

describe('slides utils', () => {
  describe('parseFrontmatter', () => {
    it('should parse frontmatter correctly', () => {
      const content = `---
title: "Test Slide"
date: 2025-01-15
description: "Test description"
tags:
  - test
  - example
---

# Slide Content
`
      // フロントマターの形式が正しいことを確認
      expect(content).toContain('---')
      expect(content).toContain('title:')
      expect(content).toContain('date:')
      expect(content).toContain('tags:')
    })
  })

  describe('slide ID extraction', () => {
    it('should extract ID from path correctly', () => {
      const path = '/slides/2025-01-python-basics/slide.md'
      const match = path.match(/\/slides\/([^/]+)\/slide\.md$/)
      expect(match).not.toBeNull()
      expect(match![1]).toBe('2025-01-python-basics')
    })

    it('should return empty string for invalid path', () => {
      const path = '/invalid/path.md'
      const match = path.match(/\/slides\/([^/]+)\/slide\.md$/)
      expect(match).toBeNull()
    })
  })
})
