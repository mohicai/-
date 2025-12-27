import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 无头模式
        context = await browser.new_context()
        page = await context.new_page()

        # 打开登录页面
        await page.goto("https://skyvpnx.com/auth/login")
        await page.wait_for_load_state("networkidle")

        # 打印页面 HTML 前 500 字，确认是否是 Cloudflare 验证页
        html = await page.content()
        print("=== 登录页面 HTML 前 500 字 ===")
        print(html[:500])

        try:
            # 等待输入框出现
            await page.wait_for_selector("#email", timeout=60000)
            await page.fill("#email", os.environ["EMAIL"])
            await page.fill("#password", os.environ["PASSWORD"])

            # 点击登录按钮
            await page.click("#login_submit")
            await page.wait_for_load_state("networkidle")

            # 跳转到订阅页面
            await page.goto("https://skyvpnx.com/user")
            html_after = await page.content()
            print("=== 登录后页面 HTML 前 500 字 ===")
            print(html_after[:500])

            if "订阅" in html_after or "用户中心" in html_after:
                print("ok")
            else:
                print("登录失败")
        except Exception as e:
            print("未找到登录表单，可能还在 Cloudflare 验证页:", e)

        await browser.close()

asyncio.run(main())