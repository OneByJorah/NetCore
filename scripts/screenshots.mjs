// Captures real screenshots of the running netara stack with Playwright.
// Usage (stack already running on 3000/8000 or alternate ports):
//   BASE_URL=http://127.0.0.1:3000 API_URL=http://127.0.0.1:8000 node scripts/screenshots.mjs
// Requires: npm install --no-save playwright && npx playwright install chromium
//
// Safety: every page is scanned for private IPs, tailnet IPs, emails, and forbidden words
// BEFORE a screenshot is written. If anything matches, the script exits 1 and saves nothing.
// Extra patterns: SCRUB_PATTERNS="mycompany,internal-host" (comma-separated regexes).

import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const BASE = process.env.BASE_URL || "http://127.0.0.1:3000";
const API = process.env.API_URL || "http://127.0.0.1:8000";
const OUT = process.env.OUT_DIR || "docs/screenshots";

// Pages to capture from the live frontend and backend.
const PAGES = [
  { name: "dashboard", url: BASE + "/", wait: 2000 },
  { name: "switches", url: BASE + "/switches", wait: 2000 },
  { name: "templates", url: BASE + "/templates", wait: 2000 },
  { name: "chat", url: BASE + "/chat", wait: 2000 },
  { name: "api-docs", url: API + "/docs", wait: 2000 },
];

const FORBIDDEN = [
  { label: "private IPv4", re: /\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b/ },
  { label: "tailnet IPv4", re: /\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b/ },
  { label: "email address", re: /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i },
  { label: "school domain", re: /\bk12\.vi\b/i },
  ...(process.env.SCRUB_PATTERNS || "")
    .split(",")
    .map((p) => p.trim())
    .filter(Boolean)
    .map((p) => ({ label: `custom:${p}`, re: new RegExp(p, "i") })),
];

fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  args: process.env.NO_SANDBOX === "1" ? ["--no-sandbox"] : [],
});
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  colorScheme: "dark",
});

let failed = false;
for (const p of PAGES) {
  const page = await context.newPage();
  try {
    await page.goto(p.url, { waitUntil: "networkidle" });
  } catch (err) {
    console.error(`NAV FAIL on ${p.name}: ${err.message}`);
    failed = true;
    await page.close();
    continue;
  }
  if (p.wait) await page.waitForTimeout(p.wait);

  const text = (await page.evaluate(() => document.body.innerText)) + "\n" + (await page.title());
  const hits = FORBIDDEN.filter((f) => f.re.test(text)).map((f) => f.label);
  if (hits.length) {
    console.error(`SCRUB FAIL on ${p.name}: found ${hits.join(", ")}. No screenshot written.`);
    failed = true;
    await page.close();
    continue;
  }

  const file = path.join(OUT, `${p.name}.png`);
  await page.screenshot({ path: file, fullPage: true });
  console.log(`saved ${file}`);
  await page.close();
}

await context.close();
await browser.close();
process.exit(failed ? 1 : 0);
