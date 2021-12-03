import datetime
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5036320593:AAG8Ccs2D_x8opgsHzObd4EjGr0_KSQUpd8'
weather_token = "e0c11591b47c05f969e871dd6159a74c"
weather_smile = {
    "Clear" : "Ясно \U00002600",
    "Clouds" : "Облачно \U00002601",
    "Rain" : "Дождь \U00002614",
    "Drizzle" : "Дождь \U00002614",
    "Thunderstorm" : "Гроза \U000026A1",
    "Snow" : "Снег \U0001F328",
    "Mist" : "Туман \U0001F328"
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Для начала работы ознакомтесь со справкой, написав /help.")
    reply = "С помощью кнопки ниже можно поделиться геолокицией с ботом."
    await message.answer(reply, reply_markup=get_keyboard())


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Для показа погоды просто напишите название города в формате: Kiev, Днепр и т.д."
                        "\n\nДля отображения погоды на ближайщей к вам станции сначала нужно поделиться геолокацией,"
                        " после написать /myweather.")


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("Поделиться", request_location=True)
    keyboard.add(button)
    return keyboard


lat = None
lon = None


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    global lat, lon
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer("Теперь вы можете использовать команду /myweather.")


@dp.message_handler(commands=['myweather'])
async def myweather(message: types.Message):
    try:
        global lat, lon
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}"
            f"&units=metric&lang='ru'"
        )
        data = r.json()

        weather_desc = data['weather'][0]['main']
        if weather_desc in weather_smile:
            wd = weather_smile[weather_desc]
        else:
            wd = "Чёт нифига не понятно, посмотри в окно."

        temp = data['main']['temp']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%d-%m-%Y %H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%d-%m-%Y %H:%M')
        day_length = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                     datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        tip = "Хорошего дня!"
        if temp < 6 and temp > 0:
            tip = "Сегодня прохладно, оденьтесь потеплее <3"
        elif temp > 6 and temp < 15:
            tip = "Неплохая погодка, могло быть хуже, выше нос!"
        elif temp > 15 and temp < 21:
            tip = "Приятная погодка, хорошего дня!"
        elif temp > 21 and temp < 30:
            tip = "Замечательная погода, не сидите дома!"
        elif temp > 30:
            tip = "Ого, вот это жара!"
        elif temp < 0 and temp > -10:
            tip = "На улице меньше нуля, оденьтесь теплее."
        elif temp < -10:
            tip = "Лучше остаться дома."

        await message.answer(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***"
                             f"\nГород: {data['name']}"
                             f"\nТемпература: {temp}°C, "f"{wd}"
                             f"\nВлажность: {data['main']['humidity']}%"
                             f"\nДавление: {data['main']['pressure']} мм.рт.ст"
                             f"\nВетер: {data['wind']['speed']} м/с "
                             f"\nРассвет: {sunrise} "
                             f"\nЗакат: {sunset}"
                             f"\nПродолжительность дня: {day_length}"
                             f"\n{tip}")
    except Exception as ex:
            await message.answer("Сначала поделитесь геолокацией.")



@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text.lower()}&appid={weather_token}"
            f"&units=metric&lang='ru'"
        )
        data = r.json()

        weather_desc = data['weather'][0]['main']
        if weather_desc in weather_smile:
            wd = weather_smile[weather_desc]
        else:
            wd = "Чёт нифига не понятно, посмотри в окно."

        temp = data['main']['temp']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%d-%m-%Y %H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%d-%m-%Y %H:%M')
        day_length = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                     datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        tip = "Хорошего дня!"
        if temp < 6 and temp > 0:
            tip = "Сегодня прохладно, оденьтесь потеплее <3"
        elif temp > 6 and temp < 15:
            tip = "Неплохая погодка, могло быть хуже, выше нос!"
        elif temp > 15 and temp < 21:
            tip = "Приятная погодка, хорошего дня!"
        elif temp > 21 and temp < 30:
            tip = "Замечательная погода, не сидите дома!"
        elif temp > 30:
            tip = "Ого, вот это жара!"
        elif temp < 0 and temp > -10:
            tip = "На улице меньше нуля, оденьтесь теплее."
        elif temp < -10:
            tip = "Лучше остаться дома."

        await message.answer(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***"
                             f"\nГород: {data['name']}"
                             f"\nТемпература: {temp}°C, "f"{wd}"
                             f"\nВлажность: {data['main']['humidity']}%"
                             f"\nДавление: {data['main']['pressure']} мм.рт.ст"
                             f"\nВетер: {data['wind']['speed']} м/с "
                             f"\nРассвет: {sunrise} "
                             f"\nЗакат: {sunset}"
                             f"\nПродолжительность дня: {day_length}"
                             f"\n{tip}")
    except Exception as ex:
        await message.answer("Такого города не существует :(")
        print(ex)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)