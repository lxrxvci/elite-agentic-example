import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Header } from '@/widgets/Header/Header'

describe('Header', () => {
  it('renders the title', () => {
    render(<Header title="Test Title" />)
    expect(screen.getByText('Test Title')).toBeDefined()
  })
})
