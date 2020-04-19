import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text == 'Как дела?':
        bot.send_message(message.chat.id, 'Норм')
    else:
        bot.send_message(message.chat.id, 'Не понимаю :(')


# RUN
bot.polling(none_stop=True)
