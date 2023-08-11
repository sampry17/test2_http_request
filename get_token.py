from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from config import path_driver
from fake_useragent import UserAgent
from json import loads


def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--user-agent={UserAgent().random}')

    s = Service(
        executable_path=path_driver
    )

    return webdriver.Chrome(
        service=s,
        options=chrome_options,
    )


def token_auth():
    try:
        with get_chromedriver() as browser:
            url = 'https://www.maxmind.com/en/locate-my-ip-address'
            browser.get(url=url)

            for request in browser.requests:
                if request.method == 'POST' and request.url == 'https://www.maxmind.com/en/geoip2/demo/token':
                    post_request = request
                    break

            if post_request:
                response = post_request.response
                token = loads(response.body)['token']

            return token
    except Exception as e:
        print(e)



