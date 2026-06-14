# -*- coding: utf-8 -*-
"""
Capture DEPLOYED screenshots (Tasks 25-28).

Usage:
  1. Deploy the app to Render/Railway/Heroku/Code Engine first.
  2. Set environment variable DEPLOY_URL to your deployment URL
     (e.g. https://cardealer-capstone.onrender.com).
  3. Run this script - it will save:
       deployed_landingpage.png     (Task 25)
       deployed_loggedin.png        (Task 26)
       deployed_dealer_detail.png   (Task 27)
       deployed_add_review.png      (Task 28)
"""
import sys
import os
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DEPLOY_URL = os.environ.get("DEPLOY_URL", "").rstrip("/")
OUT = r"c:\Users\exorc\Downloads\ABC"

if not DEPLOY_URL:
    print("ERROR: Set DEPLOY_URL environment variable first, e.g.")
    print("  $env:DEPLOY_URL='https://your-app.onrender.com'")
    print("  python capture_deployment_screenshots.py")
    sys.exit(1)

import asyncio
from playwright.async_api import async_playwright


async def add_url_banner(page, label):
    url = page.url
    await page.add_style_tag(content="""
        #__url_banner__ {
            position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
            background: #111; color: #fff; font: 14px/1.6 'Consolas', monospace;
            padding: 6px 12px; text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,.4);
        }
        body { padding-top: 36px !important; }
    """)
    await page.evaluate(
        """({label, url}) => {
            const div = document.createElement('div');
            div.id = '__url_banner__';
            div.textContent = `${label}  |  Endpoint: ${url}`;
            document.body.prepend(div);
        }""",
        {"label": label, "url": url},
    )
    await page.wait_for_timeout(200)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await ctx.new_page()

        # ---- Task 25: deployed_landingpage.png (home, not logged in) ----
        await page.goto(f"{DEPLOY_URL}/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(800)
        await add_url_banner(page, "Deployed landing page")
        await page.screenshot(path=os.path.join(OUT, "deployed_landingpage.png"), full_page=True)
        print("[OK] deployed_landingpage.png (Task 25)")

        # ---- Task 26: deployed_loggedin.png (logged in) ----
        await page.goto(f"{DEPLOY_URL}/djangoapp/login")
        await page.evaluate("""async () => {
            await fetch('/djangoapp/login', {
                method: 'POST', credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userName: 'testuser', password: 'TestPass123' })
            });
        }""")
        await page.goto(f"{DEPLOY_URL}/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(800)
        await add_url_banner(page, "Deployed app (Logged-in as testuser)")
        await page.screenshot(path=os.path.join(OUT, "deployed_loggedin.png"), full_page=True)
        print("[OK] deployed_loggedin.png (Task 26)")

        # ---- Task 27: deployed_dealer_detail.png ----
        await page.goto(f"{DEPLOY_URL}/djangoapp/dealer/1/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(800)
        await add_url_banner(page, "Deployed dealer detail page")
        await page.screenshot(path=os.path.join(OUT, "deployed_dealer_detail.png"), full_page=True)
        print("[OK] deployed_dealer_detail.png (Task 27)")

        # ---- Task 28: deployed_add_review.png ----
        await page.goto(f"{DEPLOY_URL}/djangoapp/dealer/1/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(500)
        await page.evaluate("document.querySelector('.post-review')?.scrollIntoView()")
        await page.fill('textarea[name="review"]', 'Excellent customer service, highly recommend this dealer!')
        await page.fill('input[name="car_year"]', '2024')
        await page.check('input[name="purchase"]')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(2500)
        await add_url_banner(page, "Deployed app - review posted")
        await page.screenshot(path=os.path.join(OUT, "deployed_add_review.png"), full_page=True)
        print("[OK] deployed_add_review.png (Task 28)")

        await browser.close()


asyncio.run(main())
