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
    global weather_c
    #print(weather_c)
    weather_c = True


@bot.message_handler(func=(lambda _ : weather_c), content_types=["location"])
def repeat_all_messages(message):
    template_en =['City: ','Current weather: ','temperature: ','pressure: ','wind: ', 'sunrise: ','sunset: ']
    template_ru = ['Город: ','Текущая погода: ','температура: ','давление: ','ветер: ','восход: ','закат: ']
    template_dim_ru = [' мм',' м/с']
    template_dim_en =[' mm',' m/sec']
    print('Checked')
    obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
    w = obs.get_weather()
    print("Checked")
    temp = w.get_temperature(unit='celsius')
    template = template_ru
    template_dim = template_dim_ru
    text = template[0] + obs.get_location().get_name() + '\n' \
              + template[1] +'\n' \
              + w.get_detailed_status() + '\n' \
              + template[2] + str(temp['temp']) + " °C" + '\n' \
              + template[3] + str(round(w.get_pressure()['press']/1.333224)) + template_dim[0]+'\n' \
              + template[4] + str(w.get_wind()['speed']) + template_dim[1] +'\n' \
              + template[5] + datetime.fromtimestamp(w.get_sunrise_time()).strftime('%H:%M:%S') + '\n' \
              + template[6] + datetime.fromtimestamp(w.get_sunset_time()).strftime('%H:%M:%S')
    bot.send_message(message.chat.id, text)
    global weather_c
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
    bot.polling(none_stop=True)

