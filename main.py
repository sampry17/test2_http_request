import requests
from bs4 import BeautifulSoup
from proxy import login, password, proxy_ip, proxy_port


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization": "Bearer v2.local.b2B-uWjXw-epMgZP77NI6iBbTM6ppr4EP6JCrS9xKFV0nwltmrPLiq-L4AJUrE1783GSdHrkAS9f2WdrCSoJejf0xCWRXcs_To3TDceW6gtuKb5ztQE6pE_gtFbNRbkslTaM24XUEKsSlOCv9q_WsdxhhaWHNFsTINO9qv6zfsDsuNDTyK8XsqGJMJ_LlPHICTK2GMOrBMQaoQ62",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.685 Yowser/2.5 Safari/537.36'
}

proxies = {
    'http': f'http://{login}:{password}@{proxy_ip}:{proxy_port}',
    'https': f'http://{login}:{password}@{proxy_ip}:{proxy_port}',
}


def get_list_regions(url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
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


def get_ip(url):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'lxml')

    ip = soup.select_one('#d_clip_button').text.strip()

    print(f'IP: {ip}')
    return ip


def get_time_zone_name(url):
    response = requests.get(url=url, headers=headers, proxies=proxies).json()
    time_zone = response['location']['time_zone']
    return time_zone


def main():
    ip = get_ip(url='https://2ip.ru/')
    time_zone = get_time_zone_name(url=f'https://geoip.maxmind.com/geoip/v2.1/city/{ip}?demo=1')
    timezones_dict = get_list_regions(url='https://gist.github.com/salkar/19df1918ee2aed6669e2')

    with open('result.txt', 'w') as file:
        regions = timezones_dict[time_zone] if time_zone in timezones_dict.keys() else 'Нет регионов'
        file.write(f'{str(time_zone)}\n{regions}')


if __name__ == '__main__':
    main()