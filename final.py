import requests
import sys
import random
import urllib3
import datetime
import time
import json
import string
import pyqrcode
import png
import datetime
import colorama
from colorama import Fore, Back, Style
colorama.init()
print(Fore.GREEN)
apikey ='' #Ключ с сайта smsactivate
if apikey=='':
	apikey=input("Вставьте ключ с smsactivate:")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
a=int(input("Сколько qr кодов хотите получить "))
def macdac():
	i=0
	smsActivateStart = f"https://sms-activate.ru/stubs/handler_api.php?api_key={apikey}&action=getNumber&service=ry&country=0"
	MacdacLogin = 'https://mobile-api.mcdonalds.ru/api/v1/user/login/phone'
	KEY_LEN = 16
	randomN1=random.randint(1000000000000,9999999999999)
	randomN2=random.randint(1000000000000,9999999999999)
	z=str(randomN1)
	s=str(randomN2)
	randomN3=z+'-'+s
	def base_str():
		return (string.hexdigits)
	oppp = random.choices(base_str(), k=KEY_LEN)
	deviceid = (''.join(oppp))
	deviceid = deviceid.lower()
	headers = {
		'X-Device-ID': deviceid,
		'X-Device-Model': 'HTC6525LVW',
		'X-Platform': 'Android',
		'X-OS-Version': '25',
		'X-Language': 'ru_RU',
		'X-App-Version': '7.6.0',
		'X-Build-Number': '3689',
		'X-Cellular-Name': 'MTS',
		'X-City-ID': '5dfc9fdc51f0dc92455beefa',
		'X-Timezone': 'GMT+03:00',
		'X-Appsflyer-ID': randomN3,
		'Content-Type': 'application/json; charset=UTF-8',
		'Content-Length': '24',
		'Host': 'mobile-api.mcdonalds.ru',
		'Connection': 'Keep-Alive',
		'Accept-Encoding': 'gzip',
		'User-Agent': 'okhttp/3.12.1'
		}
	r2 = requests.post(smsActivateStart, verify=False) #Запрос на получение номера
	response_r2 = r2.text #Преобразование ответа с сайта в текст
	if response_r2 == 'NO_NUMBERS':
		print('Номеров нету ',i)
		i=i+1
		macdac()
	if response_r2 == 'NO_BALANCE':
		sys.exit('че с деньгами(их нет)')
	else: #Выделенеие номера
		ACCESS_NUMBER = r2.text
		start_number = ACCESS_NUMBER.find(':7')
		null = ACCESS_NUMBER[14:start_number]
		aaa = start_number + 1
		number = ACCESS_NUMBER[aaa:36]
	time.sleep(5)
	print("header=",headers)
	numberres = "+" + number
	print(numberres)
	url3 = f'https://sms-activate.ru/stubs/handler_api.php?api_key={apikey}&action=setStatus&status=1&id={null}'
	print('Сплю 30 секунд, чтобы не получить блокировку в маке')
	time.sleep(30)
	r1 = requests.post(MacdacLogin, verify=False, headers=headers, json={"phone": numberres})
	if r1.status_code == 429:
		sys.exit('Слишком много запросов, нужно подождать и снова запустить программу')
	print('Номер успешно получен! Вбиваю номер в мак.')
	print("deviceid=",deviceid)
	res = json.loads(r1.text)
	time.sleep(5)
	r3 = requests.post(url3, verify=False)
	print('Сплю 30 секунд и проверяю номер на наличие смс')
	time.sleep(30)
	url4 = f'https://sms-activate.ru/stubs/handler_api.php?api_key={apikey}&action=getStatus&id={null}'
	def sms(url):
		s=False
		z=0
		while s!="True":
			sleep(30)
			i+=1
			r4 = requests.post(url, verify=False)
			str = 'STATUS_OK'
			for s in r4.text:
				if str.lower().find(s.lower()) != -1: #Проверка смс
					s = 'True'
					break
			if s == 'True':
				CODE = r4.text[10:14]
				print(CODE)
			if z == 5:
				print("Смс не пришла.")
				macdac()
		return CODE
	CODE=sms(url14)
	print('Нашел смс! Подтверждаю номер в маке.')
	url5 = 'https://mobile-api.mcdonalds.ru/api/v1/user/login/phone/confirm'
	r5 = requests.post(url5, verify=False, headers=headers, json={"code": CODE}) #Подтверждение регистрации при помощи кода из смс
	print("r5",r5.text)
	res2 = json.loads(r5.text)
	token = res2['token']
	print("token-",token)
	time.sleep(5)
	headersonlog = {
	'X-Device-ID': deviceid,
	'X-Device-Model': 'HTC6525LVW',
	'X-Platform': 'Android',
	'X-OS-Version': '25',
	'X-Language': 'ru_RU',
	'X-App-Version': '7.6.0',
	'X-Build-Number': '3689',
	'X-Cellular-Name': 'MTS',
	'X-City-ID': '5dfc9fdc51f0dc92455beefa',
	'X-Timezone': 'GMT+03:00',
	'X-Appsflyer-ID': randomN3,
	'authorization': "Bearer "+token,
	'Host': 'mobile-api.mcdonalds.ru',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip, deflate',
	'User-Agent': 'okhttp/3.12.1'}
	print("headersonlogd-",headersonlog)
	print("jdu10sec")
	time.sleep(10)
	url6 = f'https://mobile-api.mcdonalds.ru/api/v1/offers/offer/22907353/qr'
	print('получаю qr')
	r6 = requests.get(url6, verify=False, headers=headersonlog)
	print("r6-",r6.text)
	res3 = json.loads(r6.text)
	isActive = res3['isActive']
	qrcode= res3['code']
	a = a - 1
while a>0:
	macdac()
	a-=1