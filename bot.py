# -*- coding: utf-8 -*-
import config
import telebot
import logging
from datetime import datetime
from pyowm import OWM

bot = telebot.TeleBot(config.telegramToken)
owm = OWM(API_key=config.owmToken, language='ru')
weather_c = False
commands = ['start', 'spacite', 'help']


@bot.message_handler(commands=['start'])
def starting_func(message):
    bot.send_message(message.chat.id, 'KOLOBOK')


@bot.message_handler(commands=['help'])
def print_commandslist(message):
    for i in commands:
        bot.send_message(message.chat.id, i)


@bot.message_handler(commands=['getWeather', 'getweather', 'weather'])
def get_weather(message):
    bot.send_message(message.chat.id, "Enter taget location")
    weather_c = True
    g = lambda flag: flag
    print(g(weather_c))


@bot.message_handler(func=(lambda flag: flag)(weather_c), content_types=["location"])
def repeat_all_messages(message):
    obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
    w = obs.get_weather()
    print("Checked")
    temp = w.get_temperature(unit='celsius')
    text_en = 'City: ' + obs.get_location().get_name() + '\n' \
              + 'Current weather:\n' \
              + w.get_detailed_status() + '\n' \
              + 'temperature: ' + str(temp['temp']) + unicode(' °C', 'utf-8') + '\n' \
              + 'min: ' + str(temp['temp_min']) + unicode(' °C', 'utf-8') + '\n' \
              + 'max: ' + str(temp['temp_max']) + unicode(' °C', 'utf-8') + '\n' \
              + 'pressure: ' + str(w.get_pressure()['press']) + ' mm\n' \
              + 'wind: ' + str(w.get_wind()['speed']) + 'm/sec\n' \
              + 'sunrise: ' + datetime.fromtimestamp(w.get_sunrise_time()).strftime('%H:%M:%S') + '\n' \
              + 'sunset: ' + datetime.fromtimestamp(w.get_sunset_time()).strftime('%H:%M:%S')
    bot.send_message(message.chat.id, text_en)
    weather_c = False


@bot.message_handler(content_types=['sticker'])
def repeat_sticker(message):
    stickers = bot.get_sticker_set(message.sticker.set_name)
    for i in range(10) if len(stickers.stickers) > 10 else range(len(stickers.stickers)):
        bot.send_sticker(message.chat.id, stickers.stickers[i].file_id)


# @bot.message_handler(content_types=['venue'])
# def get_venue(message):
#     print('Venue carried')
#     bot.send_message(message.chat.id, message.venue.address)
# @bot.message_handler(content_types=['location'])
# def get_location(message):
#     print(message.location.latitude)
#     bot.send_message(message.chat.id, str(message.location.latitude) + " "+str(message.location.longitude))

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        print("Internet error")
