# -*- coding: utf-8 -*-
import config
import requests
from sys import argv

message = argv[1]
url = 'https://api.telegram.org/bot' + config.token + '/sendMessage'
params = {'chat_id': config.chat_id, 'text': message}
requests.post(url, data=params, proxies={'https': config.proxy})