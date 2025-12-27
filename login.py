import cloudscraper

scraper = cloudscraper.create_scraper()

login_url = "https://skyvpnx.com/auth/login"
payload = {
    "email": "2697288516@qq.com",
    "password": "asdqwe132,"
}

resp = scraper.post(login_url, data=payload)

if resp.status_code == 200 and "用户中心" in resp.text:
    print("ok")
else:
    print("登录失败:", resp.status_code)