# -*- coding: utf-8 -*-
import config
import requests
from sys import argv
import func

proxy_server = func.get_proxy_list('HTTPS')[0]
proxy_server ='https://' + proxy_server['address'] + ':' + proxy_server['port']
message = argv[1]
url = 'https://api.telegram.org/bot' + config.token + '/sendMessage'
params = {'chat_id': config.chat_id, 'text': message}
requests.post(url, data=params, proxies={'https': proxy_server})