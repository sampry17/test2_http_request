import requests
from bs4 import BeautifulSoup
from config import login, password, proxy_host, proxy_port
from get_token import token_auth


def get_session():
    session = requests.Session()

    session.headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.685 Yowser/2.5 Safari/537.36'
    }

    session.proxies = {
        'http': f'http://{login}:{password}@{proxy_host}:{proxy_port}',
        'https': f'http://{login}:{password}@{proxy_host}:{proxy_port}',
    }

    return session


def get_list_regions(url, session):
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    list_tz = ''
    elements = soup.select_one('table.highlight').select('.blob-code.blob-code-inner.js-file-line')
    for elem in elements:
        list_tz += elem.get_text()

    list_tz = eval(list_tz)

    timezones_dict = {}

    for region, timezone in list_tz:
        if timezone in timezones_dict:
            timezones_dict[timezone].append(region)
        else:
            timezones_dict[timezone] = [region]

    return timezones_dict


def get_ip(url, session):
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.select_one('#d_clip_button').text.strip()

    return ip


def get_time_zone_name(url, session):
    token = token_auth()

    headers_update = {
        "Authorization": f"Bearer {token}",
    }

    session.headers |= headers_update

    response = session.get(url=url).json()

    time_zone = response['location']['time_zone']
    return time_zone


def main():
    s = get_session()
    ip = get_ip(url='https://2ip.ru/', session=s)
    time_zone = get_time_zone_name(url=f'https://geoip.maxmind.com/geoip/v2.1/city/{ip}?demo=1', session=s)
    timezones_dict = get_list_regions(url='https://gist.github.com/salkar/19df1918ee2aed6669e2', session=s)

    with open('result.txt', 'w') as file:
        regions = timezones_dict[time_zone] if time_zone in timezones_dict.keys() else 'Нет соответствующих регионов..'
        file.write(f'{time_zone}\n{regions}')


if __name__ == '__main__':
    main()