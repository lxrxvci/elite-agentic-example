import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('login page has no detectable accessibility violations', async ({ page }) => {
  await page.goto('/login')
  await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze()
  expect(accessibilityScanResults.violations).toEqual([])
})
