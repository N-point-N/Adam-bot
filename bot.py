import config
import telebot
import logging
from pyowm import OWM

bot = telebot.TeleBot(config.token)
commands = ['start','spacite','help']
#stickers =  bot.get_sticker_set('BrotherhoodBald')



@bot.message_handler(commands=['start'])
def starting_func(message):
    bot.send_message(message.chat.id, 'KOLOBOK')
@bot.message_handler(commands=['help'])
def print_commandslist(message):
    for i in commands:
        bot.send_message(message.chat.id,i)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text + "GITtesting")

@bot.message_handler(content_types=['sticker'])
def repeat_sticker(message):
    stickers = bot.get_sticker_set(message.sticker.set_name)
    for i in range(10) if len(stickers.stickers)>10 else range(len(stickers.stickers)):
        bot.send_sticker(message.chat.id, stickers.stickers[i].file_id)




if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        print("Internet error")
