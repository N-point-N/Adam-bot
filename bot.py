import config
import telebot
import logging

bot = telebot.TeleBot(config.token)
commands = ['start','spacite','help']

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


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        print("Internet error")
