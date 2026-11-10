// Writes the link preview card: renders scripts/og-card.html at 1200 x 630 and saves site/assets/og-card-v2.png.
// Usage: node scripts/og-card.mjs   (needs Playwright with Chromium, and network access for Google Fonts)
import { createRequire } from 'node:module'
import { fileURLToPath, pathToFileURL } from 'node:url'
import path from 'node:path'

const here = path.dirname(fileURLToPath(import.meta.url))
// require() finds a Playwright installed globally as well as one in node_modules.
const { chromium } = createRequire(import.meta.url)('playwright')
const page = pathToFileURL(path.join(here, 'og-card.html')).href
const out = path.join(here, '..', 'site', 'assets', 'og-card-v2.png')

const browser = await chromium.launch()
const tab = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 })
await tab.goto(page, { waitUntil: 'networkidle' })
await tab.evaluate(() => document.fonts.ready)
await tab.screenshot({ path: out })
await browser.close()
console.log('wrote', path.relative(process.cwd(), out))
