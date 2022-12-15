import requests
import datetime

import markups as nav
import messages as msg

from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


""" подключение к боту через токен """

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет,{message.from_user.first_name}! Напиши мне название города и я пришлю сводку погоды!")

@dp.message_handler()
async def get_message(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        """Добавляет в переменную data ответ в json"""
        data = r.json()

        """Берёт информацию из переменной data.с ключом и переменной к ключу"""
        city = data["name"]
        cur_weather = data["main"]["temp"]
        temp_feels = data["main"]["feels_like"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода"

        coord_lon = data["coord"]["lon"]
        coord_lat = data["coord"]["lat"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"] * 0.75
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])


        await message.reply(f"🕰{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} 🕰\n"
              f"Погода в городе: {city}\nДолгота: {coord_lon}\nШирота: {coord_lat}\nТемпература: {cur_weather}° {wd}\n"
              f"Ощущается как: {temp_feels}°\n"
              f"Влажность:"f"{humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца:{sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Продолжительность дня:{length_of_the_day}\n"  
              f"Хорошего дня,{message.from_user.first_name }! \U0001F609"
              )
        await message.answer("Выбери команду", reply_markup=nav.mainMenu)


    except:
        if message.text == 'О боте':
            await bot.send_message(message.from_user.id, f"Какой любознательный, ну держи!\n" + msg.text, reply_markup=nav.mainMenu)

        elif message.text == 'Помогите!':
            await bot.send_message(message.from_user.id, msg.help_text, reply_markup=nav.mainMenu)

        elif message.text == 'проблема с ботом':
            await bot.send_message(message.from_user.id, msg.help_text2, reply_markup=nav.mainMenu)

        elif message.text == 'Меню':
            await bot.send_message(message.from_user.id, msg.main_menu, reply_markup=nav.mainMenu)

        elif message.text == 'Крутой бот':
            await message.reply(f'Спасибо❤️')

        elif message.text == 'Что умеешь делать?':
            await message.reply(f'{msg.what_you_do}',reply_markup=nav.mainMenu)

        else:
            await message.reply(f"{msg.wrong_message}\n"
            f"\U00002620 Проверьте название города \U00002620")
        print('Сработало исключение')

if __name__ == '__main__':
    executor.start_polling(dp)
