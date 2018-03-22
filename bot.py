# -*- coding: utf-8 -*-
import config
import telebot
from datetime import datetime
from pytz import timezone
from timezonefinder import TimezoneFinder
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


@bot.message_handler(commands=['weather'])
def get_weather(message):
    # ==================================DESCRIPTION=======================================
    text_en = 'Enter target location: '
    text_ru = 'Укажите нужное местоположение: '
    text_btn_en = 'Enter my location'
    text_btn_ru = 'Отправить мои координаты'
    # ==================================INIT TEXT=========================================
    text = text_ru
    text_btn = text_btn_ru
    # ==================================START HANDLER=====================================
    global weather_c
    weather_c = True
    lc_btn = telebot.types.KeyboardButton(text=text_btn, request_location=True)
    lc_krd = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    lc_krd.add(lc_btn)
    bot.send_message(message.chat.id, text, reply_markup=lc_krd)


@bot.message_handler(func=(lambda _: weather_c), content_types=["location"])
def repeat_all_messages(message):
    # =======================================DESCRIPTION====================================
    template_short_en = ['Current weather: ', 'temperature: ', 'precipitation expected: ', 'wind: ']
    template_short_ru = ['Текущая погода: ', 'температура: ', 'вероятность осадков: ', 'ветер: ']
    template_en = ['City: ', 'Current weather: ', 'temperature: ', 'pressure: ', 'precipitation:', 'wind: ',
                   'sunrise: ', 'sunset: ']
    template_ru = ['Город: ', 'Текущая погода: ', 'температура: ', 'давление: ', 'осадки: ', 'ветер: ', 'восход: ',
                   'закат: ']
    template_dim_ru = [' мм', ' м/с']
    template_dim_en = [' mm', ' m/sec']
    # ========================================INIT TEXT======================================
    template = template_ru
    template_short = template_short_ru
    template_dim = template_dim_ru
    # ========================================START HANDLER===================================
    tf = TimezoneFinder()
    tt = timezone(tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude))
    obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
    w = obs.get_weather()
    sunrize = datetime.fromtimestamp(w.get_sunrise_time()).astimezone(tt)
    sunzet = datetime.fromtimestamp(w.get_sunset_time()).astimezone(tt)
    text_short = template_short[0] + '\n' \
                 + w.get_detailed_status() + '\n' \
                 + template_short[1] + str(w.get_temperature(unit='celsius')['temp']) + "°C" + '\n' \
                 + template_short[2] + str(w.get_clouds()) + ' %\n' \
                 + template_short[3] + str(w.get_wind()['speed']) + template_dim[1] + '\n'
    # text = template[0] + obs.get_location().get_name() + '\n' \
    #          + template[1] +'\n' \
    #          + w.get_detailed_status() + '\n' \
    #          + template[2] + str(w.get_temperature(unit='celsius')['temp']) + " °C" + '\n' \
    #          + template[3] + str(round(w.get_pressure()['press']/1.333224)) + template_dim[0]+'\n' \
    #          + template[4] + str(w.get_wind()['speed']) + template_dim[1] +'\n' \
    #          + template[5] + sunrize.strftime('%H:%M:%S') + '\n' \
    #          + template[6] + sunzet.strftime('%H:%M:%S')
    lc_krd = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text_short, reply_markup=lc_krd)
    global weather_c
    weather_c = False


@bot.message_handler(content_types=['sticker'])
def repeat_sticker(message):
    stickers = bot.get_sticker_set(message.sticker.set_name)
    for i in range(10) if len(stickers.stickers) > 10 else range(len(stickers.stickers)):
        bot.send_sticker(message.chat.id, stickers.stickers[i].file_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
