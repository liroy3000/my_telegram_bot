# -*- coding: utf-8 -*-
import telebot
import config
import func
import re

proxy_server = func.get_proxy_list('HTTPS')[0]
proxy_server ='https://' + proxy_server['address'] + ':' + proxy_server['port']
telebot.apihelper.proxy = {'https': proxy_server}
bot = telebot.TeleBot(config.token)

# Получить ip домашнего компьютера (на котором работает бот)
@bot.message_handler(commands=['ip'])
def send_ip(message):
	bot.send_message(message.chat.id, func.show_ip())

# Поставить торрент на загрузку
@bot.message_handler(content_types=['document'])
def downoal_torrent(message):
	if re.findall(r'torrent$', message.document.file_name):
		file_info = bot.get_file(message.document.file_id)
		download_file = bot.download_file(file_info.file_path)
		with open(config.torrent_path, 'wb') as new_file:
			new_file.write(download_file)
		bot.send_message(message.chat.id, 'Файл добавлен к загрузке')

	else:
		bot.send_message(message.chat.id, 'Мне нужен файл в формате .torrent') 




if __name__ == '__main__':
    bot.polling(none_stop=True)