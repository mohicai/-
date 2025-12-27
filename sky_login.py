import asyncio
from playwright.async_api import async_playwright
import os, random

async def main():
    async with async_playwright() as p:
        # 启动 Chromium，有头模式，模拟真实用户
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
            timezone_id="Asia/Shanghai"
        )
        page = await context.new_page()

        # 打开登录页面
        await page.goto("https://skyvpnx.com/auth/login")

        # 保存登录页面 HTML
        html = await page.content()
        with open("login_page.html", "w", encoding="utf-8") as f:
            f.write(html)

        try:
            # 等待输入框出现
            await page.wait_for_selector("#email", timeout=60000)
            await page.type("#email", os.environ["EMAIL"], delay=100+random.randint(0,50))
            await page.type("#password", os.environ["PASSWORD"], delay=100+random.randint(0,50))

            # 模拟鼠标点击
            await page.hover("#login_submit")
            await page.click("#login_submit")

            # 等待用户中心出现
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