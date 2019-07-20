# -*- coding: utf-8 -*-
import telebot
import config
import func

telebot.apihelper.proxy = {'https': config.proxy}
bot = telebot.TeleBot(config.token)

# Получить ip домашнего компьютера (на котором работает бот)
@bot.message_handler(commands=['ip'])
def send_ip(message):
	bot.send_message(message.chat.id, func.show_ip())









if __name__ == '__main__':
    bot.polling(none_stop=True)