import telebot
import requests
import  datetime
from config import tg_bot_token, open_weather_token
import aiogram

bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=['start'])
def start_command(message):
    text ='Привет!\nЯ бот, который может показывать погоду.\nНапишите название города, без ошибок, на кириллице или латинице'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, get_weather)

@bot.message_handler(commands=['day_long'])
def weather_command(message):
    text = 'Привет, я могу показать восход/закат солнца, а также продожительность дня в любом городе! Назови город!'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, get_long_day)


@bot.message_handler(commands=['day_long'])
def get_long_day(message):

    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()
    except Exception as ex:
       # print(ex)
        bot.send_message(message.chat.id,'\U00002620 Проверьте название города \U00002620\n Введите название города или команду /start')

    sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
    day_length = sunset_time - sunrise_time
    s = ""
    s += f"Восход солнца: {sunrise_time}\nЗаход солнца: {sunset_time}\nПродолжительность дня: {day_length}\n"
    bot.send_message(message.chat.id, s)


def get_weather(message):

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
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()

        weather_descript = data['weather'][0]['main']
        if weather_descript in code_to_smile:
            wd = code_to_smile[weather_descript]
        else:
            wd = 'Посмотри сам в окно, я не знаю что там происходит'
        #pprint(data)
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        s = ''
        s += f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
        s += f"Погода в городе: {city}\nТемпература: {cur_weather} °C {wd}\n"
        s += f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
        # s += f"Восход солнца: {sunrise_time}\nЗаход солнца: {sunset_time}\nПродолжительность дня: {day_length}\n"
        s += f"Одевайтесь по погоде! Доброго здоровья!"

        bot.send_message(message.chat.id, s)

    except Exception as ex:
        bot.send_message(message.chat.id,'\U00002620 Проверьте название города \U00002620\n Введите название города или команду /start')

bot.polling(none_stop=True, interval=0)  # Обращается к серверу телеграмм каждвые 0 мс.