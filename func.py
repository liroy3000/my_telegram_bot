# -*- coding: utf-8 -*-
from requests import get
from lxml import etree
from lxml import html
import requests
import re
import subprocess
import json
import shutil

def show_ip():
    return get('https://api.ipify.org').text

def get_proxy_list(stype='all'):

    if stype != 'HTTPS' and stype != 'HTTP' and stype != 'all':
        print ('Не верно указан тип сервера! Доступные значения: "HTTPS", "HTTP", "all"')
        exit()

    url = 'http://foxtools.ru/Proxy?al=True&am=True&ah=True&ahs=True&http=True&https=True'

    res = requests.get(url)
    res = html.fromstring(res.text)
    tbody = res.xpath('//tbody')
    trs = tbody[0].xpath('.//tr')

    server_list = []

    for line in trs:
        tds = line.xpath('.//td')

        address = re.search('>(.+?)<', str(etree.tostring(tds[1])))
        address = address.group(1)

        port = re.search('>(.+?)<', str(etree.tostring(tds[2])))
        port = port.group(1)

        if re.findall('HTTPS', str(etree.tostring(tds[5]))):
            serv_type = 'HTTPS'
        else:
            serv_type = 'HTTP'

        ping = re.search('>(.+?)<', str(etree.tostring(tds[6])))
        ping = float(ping.group(1))

        if stype == 'all' or stype == serv_type:
            server_list.append({'address': address, 'port': port, 'type': serv_type, 'ping': ping})

    server_list = sorted(server_list, key=lambda k: k['ping'])

    return server_list

def check_user(bot, message, enabled_users):
    user_id = message.from_user.id
    if user_id  in enabled_users:
        return True
    else:
        bot.send_message(message.chat.id, user_id)
        bot.send_message(message.chat.id, "Access denied.")
        return False

def torrent(arg):
    if arg == "status":
        try:
            # Выполняем команду systemctl для получения статуса
            result = subprocess.run(
                ['systemctl', 'is-active', 'qbittorrent.service'],
                capture_output=True,
                text=True,
                check=True
            )
            # Проверяем, возвращает ли команда 'active'
            if result.stdout.strip() == 'active':
                return 'running'
            else:
                return 'not running'
        except subprocess.CalledProcessError:
            return 'not running'
        except FileNotFoundError:
            return 'not running'
        except Exception as e:
            return "An unexpected error occurred: " + e
    if arg == "start":
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'qbittorrent.service'])
            return "QBitTorrent запущен."
        except:
            return "Произошла ошибка во время запуска QBitTorrent"
    if arg == "stop":
        try:
            subprocess.run(['sudo', 'systemctl', 'stop', 'qbittorrent.service'])
            return "QBitTorrent остановлен."
        except:
            return "Произошла ошибка во время остановки QBitTorrent"

def get_torrents(url):
    try:
        torrents_list = get(url + "/api/v2/sync/maindata?rid=0&lz6kxcul").json()
    except Exception as e:
        return "Похоже, QBitTorrent остановлен. Проверьте статус с помощью /torrent_status" 
    result = "Torrents:\n------\n"
    for torrent in torrents_list["torrents"]:
        result = result + torrents_list["torrents"][torrent]["name"] + "\nProgress: " + str(round(torrents_list["torrents"][torrent]["progress"]*100, 2)) + "%\n------\n"
    return result

def get_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    percent = used * 100 / total
    total = total / (1024 ** 3)
    used = used / (1024 ** 3)
    free = free / (1024 ** 3)
    return {
        'total': str(round(total, 2)),
        'used': str(round(used, 2)),
        'free': str(round(free, 2)),
        'percent': str(round(percent, 2))
    }
