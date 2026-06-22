import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('renders a label and responds to clicks', async () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Save</Button>)
    const button = screen.getByRole('button', { name: 'Save' })
    await userEvent.click(button)
    expect(handleClick).toHaveBeenCalled()
  })

  it('is disabled and shows aria-busy when loading', () => {
    render(<Button loading>Loading</Button>)
    const button = screen.getByRole('button', { name: 'Loading' })
    expect(button).toBeDisabled()
    expect(button).toHaveAttribute('aria-busy', 'true')
  })
})
