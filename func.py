# -*- coding: utf-8 -*-
from requests import get
from lxml import etree
from lxml import html
import requests
import re

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
