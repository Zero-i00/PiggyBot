import requests
import json


def get_data(c):
    response = requests.get(url=f'https://finance.rambler.ru/api/sources/cbr/instruments/{c.upper()}/?step=1&start=1651853380&end=1654445380')
    with open(f'data/{c.upper()}.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    return response.json()


def collect_data(url):
    response = requests.get(url=url)

    with open(f'news/news.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    return response.json()


def main():
    collect_data('https://zen.yandex.ru/api/v3/launcher/more?channel_name=quote.rbc.ru&clid=300&_csrf=8bfe1e072daac85eaf8e4e9382ea15d69186dcae-1654799976723-556828667-197536081636887520%3A0&country_code=ru&lang=ru')

if __name__ == '__main__':
    main()