# -*- coding: utf-8 -*-
from requests import get

def show_ip():
	return get('https://api.ipify.org').text