from bs4 import BeautifulSoup
import aiohttp
import re


async def get_csrf(session):
    async with session.get(url="https://www.maxmind.com/en/geoip2-precision-demo") as response:
        if response.status != 200:
            print(f'Статус ошибки: {response.status}')
            return None
        page = await response.text()
    soup = BeautifulSoup(page, "html.parser")
    element = soup.find('script', string=re.compile("X_CSRF_TOKEN"))
    if not element:
        return None
    return element.text.split("\"")[1]


async def get_token(session, csrf_token):
    headers = {
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9,tg;q=0.8",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrf-token": f'{csrf_token}',
        "x-requested-with": "XMLHttpRequest"
    }
    async with session.post(url="https://www.maxmind.com/en/geoip2/demo/token", headers=headers) as response:
        if response.status != 201:
            print(f'Статус ошибки: {response.status}')
            return None
        page = await response.json()
        try:
            return page['token']
        except IndexError:
            return None


async def auth_token():
    async with aiohttp.ClientSession() as session:
        csrf = await get_csrf(session)
        token = await get_token(session, csrf)
        return token

