from config import open_weather_token
from pprint import pprint
import requests
import datetime

def get_weather(city, open_weather_token):

    code_to_smile = {
        """смайлы погоды"""
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"

    }

    try:
        """отправка запроса"""
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        """получение данных в json формате"""
        data = r.json()
        pprint(data)
        """сбор данных по ключам и значениям"""
        city = data["name"]
        cur_weather = data["main"]["temp"]
        temp_feels = data["main"]["feels_like"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"] * 0.75
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        """вывод информации"""
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}° {wd}\n"
              f"Ощущается как: {temp_feels}°\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n "
              f"Восход солнца: {sunrise_timestamp}\n Закат солнца: {sunset_timestamp}\n "
              f"Продолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня! \U0001F609"
              )

    except Exception as ex:
        """Исключения"""
        print(ex)
        print("\U00002620 Проверьте название города \U00002620")

def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    """запуск бота"""
    main()
