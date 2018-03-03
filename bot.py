import config
import telebot
import logging

bot = telebot.TeleBot(config.token);


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text + "GITtesting")


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        print("Internet error")
