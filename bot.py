# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config
import func
import re
from os import system

# proxy_server = func.get_proxy_list('HTTPS')[0]
# proxy_server ='https://' + proxy_server['address'] + ':' + proxy_server['port']
# telebot.apihelper.proxy = {'https': proxy_server}

start_message = """
Привет, я помогу управлять твоим QBitTorrent сервером!
Тебе доступны следующие команды:
/torrent_status - покажет статус демона QBitTorrent
/torrent_stop - остановит демона QBitTorrent
/torrent_start - запустит службу QBitTorrent
/show_torrents - покажет список торрентов и процент загрузки
/space - покажет сколько осталось места на диске
/off - выключит сервер
/id - покажет твой telegram id
/ip - покажет текущий ip адрес сервера

Воспользуйся меню, чтобы выполнить любую команду.
"""

bot = telebot.TeleBot(config.token)

# Создание клавиатуры
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_id = types.KeyboardButton('/id')
    button_ip = types.KeyboardButton('/ip')
    button_off = types.KeyboardButton('/off')
    button_t_s = types.KeyboardButton('/torrent_status')
    button_t_d = types.KeyboardButton('/torrent_stop')
    button_t_e = types.KeyboardButton('/torrent_start')
    button_t_show = types.KeyboardButton('/show_torrents')
    button_space = types.KeyboardButton('/space')
    button_media_srv_rest = types.KeyboardButton('/mediasrv-restart')
    keyboard.add(button_id, button_ip, button_off, button_t_s, button_t_d, button_t_e, button_t_show, button_space, button_media_srv_rest)
    return keyboard


@bot.message_handler(commands=['start'])
def send_ip(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, start_message, reply_markup=create_keyboard())
# Получить свой user id
@bot.message_handler(commands=['id'])
def id(message):
    # if func.check_user(bot, message, config.enabled_users) == False:
    #     return
    user_id = message.from_user.id
    bot.reply_to(message, "Ваш user_id: " + str(user_id), reply_markup=create_keyboard())
    #bot.send_message(message.chat.id, "Меню:", reply_markup=create_keyboard())

# Получить ip домашнего компьютера (на котором работает бот)
@bot.message_handler(commands=['ip'])
def send_ip(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, func.show_ip(), reply_markup=create_keyboard())

# Поставить торрент на загрузку
@bot.message_handler(content_types=['document'])
def downoal_torrent(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    if re.findall(r'torrent$', message.document.file_name):
        file_info = bot.get_file(message.document.file_id)
        download_file = bot.download_file(file_info.file_path)
        with open(config.torrent_path, 'wb') as new_file:
            new_file.write(download_file)
        bot.send_message(message.chat.id, 'Файл добавлен к загрузке')

    else:
        bot.send_message(message.chat.id, 'Мне нужен файл в формате .torrent')

# Команда выключения компьютера
@bot.message_handler(commands=['off'])
def power_off(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, 'Компьютер будет выключен!', reply_markup=create_keyboard())
    system('sudo shutdown -P')

# Три команды для управления службой QBitTorrent - start, stop, status
@bot.message_handler(commands=['torrent_status'])
def power_off(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, 'QBitTorrent статус: ' + func.torrent("status"), reply_markup=create_keyboard())

@bot.message_handler(commands=['torrent_stop'])
def power_off(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, func.torrent("stop"), reply_markup=create_keyboard())

@bot.message_handler(commands=['torrent_start'])
def power_off(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, func.torrent("start"), reply_markup=create_keyboard())

# Получить список торрентов и прогресс загрузки.
@bot.message_handler(commands=['show_torrents'])
def shot_torrents(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, func.get_torrents(config.qbit_url), reply_markup=create_keyboard())

@bot.message_handler(commands=['space'])
def disk_space(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    output = ""
    for mount in config.mount_disk:
        output = output + "Раздел " + mount + ":\n"
        disk = func.get_disk_usage(mount)
        output = output + "Использовано: " + disk["used"] + " Gb (" + disk["percent"] + " %)\nСвободно: " + disk["free"] + " Gb\nВсего: " + disk["total"] + " Gb\n"
    bot.reply_to(message, output, reply_markup=create_keyboard())

@bot.message_handler(commands=['mediasrv-restart'])
def power_off(message):
    if func.check_user(bot, message, config.enabled_users) == False:
        return
    bot.send_message(message.chat.id, func.minidlna("restart"), reply_markup=create_keyboard())

if __name__ == '__main__':
    bot.polling(none_stop=True)
