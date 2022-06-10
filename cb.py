import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json

headers = {
    "accept": "*/*",
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64 (Edition Yx GX)',
}


def get_c_name():
    data = {}
    for c in get_c('https://finance.rambler.ru/currencies/'):
        response = requests.get(url=f'https://finance.rambler.ru/api/sources/cbr/instruments/{c.upper()}/?step=1')
        for value in response.json():
            data[value['char_code']] = value['nominative_singular']

    print(data)
    return data

def get_c(url):
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    all_c = soup.find_all('div', {'class': 'finance-currency-table__cell--code'})
    result = []
    for c in all_c:
        result.append(c.text.strip())

    return result

def get_data(c):
    response = requests.get(url=f'https://finance.rambler.ru/api/sources/cbr/instruments/{c.upper()}/?step=1&start=1')
    data = []
    for i in response.json():
        for sort_data in i['values'][:15]:
            data.append(sort_data)
    return data


def create_graphics(c):
    data = get_data(c)
    date = []
    rate = []
    for value in reversed(data[:7]):
        date_s = value['date'].split('-')
        date.append('{0}.{1}'.format(date_s[-1][:2], date_s[1]))
        rate.append(value['rate'])


    plt.xlabel('Дата')
    plt.ylabel('Значение')
    plt.title(f'{c.upper()} за неделю')
    plt.plot(date, rate, '-go', markerfacecolor='w', color='aquamarine', ms=3, mew=3, mec='blue', alpha=1, label=f'{c.upper()}')
    plt.legend()
    plt.grid(b=True, axis='y', color='azure')
    plt.savefig('data/graph.png')
    plt.show()




def main():
    get_c_name()
    pass
    # get_c(url='https://finance.rambler.ru/currencies/')
    # get_data('USD')
    # create_graphics('USD')



if __name__ == '__main__':
    main()

