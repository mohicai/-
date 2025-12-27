import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://skyvpnx.com/auth/login")

        # 保存登录页面 HTML
        html = await page.content()
        with open("login_page.html", "w", encoding="utf-8") as f:
            f.write(html)

        try:
            await page.wait_for_selector("#email", timeout=60000)
            await page.fill("#email", os.environ["EMAIL"])
            await page.fill("#password", os.environ["PASSWORD"])
            await page.click("#login_submit")

            await page.wait_for_selector("text=用户中心", timeout=60000)

            # 保存登录后页面 HTML
            html_after = await page.content()
            with open("user_page.html", "w", encoding="utf-8") as f:
                f.write(html_after)

            print("ok")
        except Exception as e:
            print("登录失败或仍在 Cloudflare 验证页:", e)

        await browser.close()

asyncio.run(main())