import emoji
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from cb import get_c, get_data, create_graphics, get_c_name
from news import collect_data
from predict import forecasts
from aiogram.utils.markdown import hbold, hlink
import datetime
import json
import time

bot = Bot(token='5591282091:AAEETd4iIaCJFaMmpP3IgtJv8GL9Z_GrWxY', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Список валют', 'Прогнозы', 'Новости']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    card = f'{hbold("Piggy")} - это бот,\n' \
           f'который поможет тебе следить за изменениями валют и актуальными новостями\n' \
           f' из мира инвестиций, трейдинга и финансов.'\

    await message.answer(card)
    await message.answer('Выберите  действие', reply_markup=keyboard)


@dp.message_handler(Text(equals='Список валют'))
async def currencies_list(message: types.Message):
    await message.answer('Поиск валют...')
    card = ''
    c = get_c_name()
    for key, value in c.items():
        card += f'{hbold(key)} - {value}\n'

    await message.answer(card)

@dp.message_handler(Text(equals='Прогнозы'))
async def currencies_list(message: types.Message):
    await message.answer('Прогнозируем...')
    await message.answer('Это займёт какое-то вермя.')
    card = ''
    data = forecasts(get_c('https://finance.rambler.ru/currencies/'))
    await message.answer('Примерные пргонозы составляются на неделю вперёд. ')
    for index, currency in enumerate(data.keys()):
        values = data[currency]
        percent = str(round(100*(values[-1]-values[0])/values[0], 2))

        if '-' in percent:
            percent = f'{percent}% {emoji.emojize(":red_circle:")}'
        else:
            percent = f'+{percent}% {emoji.emojize(":green_circle:")}'

        card = f'{hbold(currency)}\n'\
            f'{hbold("Сейчас: ")} {values[0]}₽\n' \
            f'{hbold("Будет через неделю: ")} {values[-1]}₽\n' \
            f'{hbold("Изменится на: ")} {percent}'

        if index%10 == 0:
            time.sleep(5)

        await message.answer(card)


@dp.message_handler(Text(equals='Новости'))
async def currencies_list(message: types.Message):
    await message.answer('Поиск новостей...')

    collect_data('https://zen.yandex.ru/api/v3/launcher/more?channel_name=quote.rbc.ru&clid=300&_csrf=8bfe1e072daac85eaf8e4e9382ea15d69186dcae-1654799976723-556828667-197536081636887520%3A0&country_code=ru&lang=ru')

    with open('news/news.json') as file:
        data = json.load(file)

    for index, item in enumerate(data['items'][:10]):
        title = item['title']
        description = item['text']
        link = item['share_link']

        card = f'{hbold(title)}\n'\
            f'{description}\n'\
            f'{hlink("Источник: ", link)}'

        await message.answer(card)


@dp.message_handler(Text(equals=get_c('https://finance.rambler.ru/currencies/') + list(map(str.lower, get_c('https://finance.rambler.ru/currencies/')))))
async def get_currency_list(message: types.Message):
    await message.answer('Загрузка...')
    c = get_c('https://finance.rambler.ru/currencies/') + list(map(str.lower, get_c('https://finance.rambler.ru/currencies/')))
    if message.text in c:
        data = get_data(message.text)
        card = f'{hbold("Дата: ")}{datetime.date.today()} | {datetime.datetime.now().strftime("%H:%M")}\n'\
            f'{hbold("Валюта: ")}{message.text}\n'\
            f'{hbold("Цена: ")}{round(float(data[0]["rate"]), 2)}₽'

        await message.answer(card)
        create_graphics(message.text)
        img = open('data/graph.png', 'rb')
        await bot.send_photo(message.from_user.id, img)
    else:
        await message.answer('Валюта не найдена')

def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()