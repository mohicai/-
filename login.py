import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 无头模式
        context = await browser.new_context()
        page = await context.new_page()

        # 打开登录页面
        await page.goto("https://skyvpnx.com/login")

        # 填写账号密码（从环境变量读取）
        await page.fill("#email", os.environ["EMAIL"])
        await page.fill("#password", os.environ["PASSWORD"])

        # 点击登录按钮
        await page.click("#login_submit")

        # 等待页面加载完成
        await page.wait_for_load_state("networkidle")

        # 跳转到订阅页面
        await page.goto("https://skyvpnx.com/user")
        html = await page.content()

        if "订阅" in html or "用户中心" in html:
            print("ok")
        else:
            print("登录失败")

        await browser.close()

asyncio.run(main())