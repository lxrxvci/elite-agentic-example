import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { StatusBadge } from './StatusBadge'

describe('StatusBadge', () => {
  it('renders visible text for each status', () => {
    render(<StatusBadge status="paid" />)
    expect(screen.getByText('Paid')).toBeVisible()
  })
})
