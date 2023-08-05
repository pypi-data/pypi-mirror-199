from selenium import webdriver


def get_xueqiu_token():
    browser = webdriver.Chrome()
    browser.get("https://www.xueqiu.com")
    cookies = browser.get_cookies();
    token = None
    for cookie in cookies:
        if cookie['name'] == 'xq_a_token':
            token = cookie['value']

    browser.close()
    return token

token = get_xueqiu_token()
print(token)