import re
import subprocess
import time
import winsound
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import string
import secrets
import random
import time
import openpyxl
import win32com
import xl
import re
import subprocess
import chardet
import psutil
import pyautogui
import pyscreeze
import datetime
import jpholiday
import email
from pyscreeze import ImageNotFoundException
from email.header import decode_header
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION=True



"""------------------------------
from my_module import my_function
でインポートして
my_function.関数名()
で使う
bt = my_function.LCOS(bid_dir,0,0,1024,768)
とか
------------------------------"""


"""------------------------------
chromeのページ読み込み待ち
------------------------------"""
def browser_load_wait(driver):
	try:
		WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located)
		result = '読込OK ' + driver.title
	except TimeoutException:
		result = "タイムアウト " + driver.title
	except NoSuchElementException:
		result = "エレメントが見つからない " + driver.title
	time.sleep(1)
	return result


"""------------------------------
secretsは暗号学的に強い乱数を作成できるらしい
推奨は英数12文字以上
記号が必要な場合は第二引数に必要な記号を記入する

やる事
記号と数字が一定数以上含まれていることを確認して足りない場合は再作成する
------------------------------"""
def pass_gen(size,symbol):
	# string.ascii_uppercase→アルファベット大文字
	# string.ascii_lowercase→アルファベット小文字
	# string.digits→数字
	chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + symbol
	while True:
		cre_pass = ''.join(secrets.choice(chars) for pass_size in range(size))
		# 数字が含まれていなければ再作成
		if re.search("[0-9]", cre_pass):
			break
		else:
			time.sleep(0.1)
	return cre_pass


'''
Tor経由でchromeでページを開く
IP変えたい場合はdriver.quit()して、再度chrome_connect_tor()を実行する

引数→無し
戻り値→driver

使用例
driver = my_function.chrome_connect_tor()
url = 'https://www.ugtop.com/spill.shtml'
driver.get(url)
print(my_function.browser_load_wait(driver) )
time.sleep(5)
driver.quit()
'''
def chrome_connect_tor():
	subprocess.Popen("taskkill /f /im tor.exe")
	time.sleep(1)
	subprocess.Popen(r"C:\Users\YUTANAO\PycharmProjects\Tor\tor.exe")
	# chromeでTor経由で起動する
	PROXY = "socks5://127.0.0.1:9050"
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--proxy-server=%s' % PROXY)
	chrome_options.add_argument('--dns-prefetch-disable')
	# chrome_options.add_argument('--headless')
	driver = webdriver.Chrome(options=chrome_options)
	return driver


'''
requestsでAPIを使用してTorで接続したときのIPアドレスを取得する
'''
def Tor_IPaddr():
	res_proxies = {
		'http': 'socks5://127.0.0.1:9050',
		'https': 'socks5://127.0.0.1:9050'
	}
	ipaddr = requests.get('http://ifconfig.me/all.json', proxies=res_proxies).json()['ip_addr']
	return ipaddr


'''
コマンドラインでフルパス取得する？
指定したフルパスが含まれるまで待つ

fullpass → 実行されるまで待つフルパス名
'''
def now_cmd_fullpass(fullpass):

	while True:
		prcm = ''

		for proc in psutil.process_iter():
			try:
				prcm = prcm + str(proc.cmdline())
			except psutil.AccessDenied:
				pass

		prcm = prcm.replace('\\\\', "\\")

		if fullpass in prcm:
			print('OK')
			break
		else:
			print('NG')
			time.sleep(1)


"""------------------------------
locateCenterOnScreen の改良版

LCOS(画像のパス,左上X座標,左上Y座標,右下X座標,右下Y座標)

returnで画像の中心座標と、false返すのでifで分岐できる
regionで幅と高さじゃなくて、ペイントで表示される座標だけ入力すればいい

bt = my_function.LCOS(bid_dir,0,0,1024,768)
if bt != False:
	print(bt)
else:
	print("none")
とかで使うといい
------------------------------"""
def LCOS(img_path,reg1,reg2,reg3,reg4):
	reg3 = reg3 - reg1
	reg4 = reg4 - reg2
	try:
		bt = pyautogui.locateCenterOnScreen(img_path,region=(reg1,reg2,reg3,reg4),confidence=0.95)
		return bt
	except ImageNotFoundException:
		return False


"""------------------------------
https://qiita.com/hid_tanabe/items/3c5e6e85c6c65f7b38be
ここを参考にした

8桁文字列形式の日付(DATE = "yyyymmdd")から
平日→False、土日祝→True
を返す関数

IPOの日付は2020/07/0とか「/」入っているので置き換える処理追加した
------------------------------"""
def isHoliDay(DATE):
	DATE = DATE.replace("/", "")
	date_time = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
	if date_time.weekday() >= 5 or jpholiday.is_holiday(date_time):
		return True
	else:
		return False


"""------------------------------
pop3でメールを受信する

https://qiita.com/jsaito/items/a058611cf9386addbc12
ここを参考にした

戻り値
受信したメルの
From ヘッダ（差出人）
Date ヘッダ（送信日時）
Subject ヘッダ（件名）
本文

メル受信したり件数取得したいたびに実行する必要有るので変数に入れたほうが楽
pop3_serv = 'pop.mail.yahoo.co.jp'
pop3_user = 'trashmail_receive_001'
pop3_pass = 'j50fBU1PvH'
cli = poplib.POP3(pop3_serv)
cli.user(pop3_user)
cli.pass_(pop3_pass)

受信したいメルの順番は受信した順番が古いほど数字が小さくなる→1番古いのは1
from_, date, subject, content
の順でタプルで入っているので
msg = my_function.fetchmail(cli, 受信したいメルの順番)[3]
print(msg)
にすると本文をプリントできる
------------------------------"""
# メールを受信する
def fetchmail(cli, msg_no):
	content = cli.retr(msg_no)[1]
	msg = email.message_from_bytes(b'\r\n'.join(content))
	# From ヘッダ（差出人）
	from_ = get_header(msg, 'From')
	# Date ヘッダ（送信日時）
	date = get_header(msg, 'Date')
	# Subject ヘッダ（件名）
	subject = get_header(msg, 'Subject')
	# 本文
	content = get_content(msg)
	return from_, date, subject, content
# ヘッダを取得
def get_header(msg, name):
	header = ''
	if msg[name]:
		for tup in decode_header(str(msg[name])):
			if type(tup[0]) is bytes:
				charset = tup[1]
				if charset:
					header += tup[0].decode(tup[1])
				else:
					header += tup[0].decode()
			elif type(tup[0]) is str:
				header += tup[0]
	return header
# 本文を取得
def get_content(msg):
	charset = msg.get_content_charset()
	payload = msg.get_payload(decode=True)
	try:
		if payload:
			if charset:
				return payload.decode(charset)
			else:
				return payload.decode()
		else:
			return ""
	except:
		return payload # デコードできない場合は生データにフォールバック


"""------------------------------
smtpでメールを送信する

https://www.python.ambitious-engineer.com/archives/2034
https://whatsnewmail.yahoo.co.jp/yahoo/20200824a.html
ここを参考にした
サンプルはなぜかstmpしかなかった

実際に使えそうなのはoutlookくらいだった

↓こういう感じで使う
# 送受信先
to_email="yutaka_yutakann@yahoo.co.jp"
# 内容
subject="あああ"
message="えええ"
my_function.outlook_mail_send_smtp_starttls(account,password,to_email,subject,message)

msg=MIMEText(message,"plain")で"plain"を指定しているので、本文に\nが入っていると改行になる
------------------------------"""
def yahoo_mail_smtp_send(account,password,to_email,subject,message):
	import smtplib,ssl
	from email.mime.text import MIMEText

	# 送信元
	from_email=account+"@yahoo.co.jp"

	# MIMEの作成
	msg=MIMEText(message,"html")
	msg["Subject"]=subject
	msg["To"]=to_email
	msg["From"]=from_email

	server=smtplib.SMTP_SSL("smtp.mail.yahoo.co.jp",465,context=ssl.create_default_context())

	server.login(account,password)
	server.send_message(msg)
	server.quit()
def danwin_mail_smtp_ssl_send(to_email,subject,message):
	import smtplib,ssl
	from email.mime.text import MIMEText

	account="w31eo5bb08t3wlqtg8lg"
	password="ecZCciCu9h"

	# 送信元
	from_email=account+"@danwin1210.me"

	# MIMEの作成
	msg=MIMEText(message)
	msg["Subject"]=subject
	msg["To"]=to_email
	msg["From"]=from_email

	server=smtplib.SMTP_SSL("smtp.danwin1210.me",465,context=ssl.create_default_context())

	server.login(account,password)
	server.send_message(msg)
	server.quit()
def yandex_mail_smtp_ssl_send(to_email,subject,message):
	import smtplib,ssl
	from email.mime.text import MIMEText

	account="j9fz5w65j2e9hkl2bn3q"
	password="e9j7c25w6E6l63qsUv3K"

	# 送信元
	from_email=account+"@yandex.com"

	# MIMEの作成
	msg=MIMEText(message)
	msg["Subject"]=subject
	msg["To"]=to_email
	msg["From"]=from_email

	server=smtplib.SMTP_SSL("smtp.yandex.com",465,context=ssl.create_default_context())

	server.login(account,password)
	server.send_message(msg)
	server.quit()
def outlook_mail_send_smtp_starttls(to_email,subject,message):
	from email.mime.text import MIMEText
	import smtplib

	# SMTP認証情報
	account="j9fz5w65j2e9hkl2bn3q@outlook.com"
	password="e9j7c25w6E6l63qsUv3K"

	# 送受信先
	from_email=account

	# MIMEの作成
	msg=MIMEText(message,"plain")
	msg["Subject"]=subject
	msg["To"]=to_email
	msg["From"]=from_email

	# メール送信処理
	server=smtplib.SMTP("smtp.office365.com",587)
	server.starttls()
	server.login(account,password)
	server.send_message(msg)
	server.quit()

"""------------------------------
floatで範囲を指定してランダムにスリープする
------------------------------"""
def random_sleep(min_time,max_time):
	random_sec=random.uniform(min_time,max_time)
	time.sleep(random_sec)
	pri=str(random_sec)+" 秒間スリープ"
	return pri


"""------------------------------
インターネットに繋がり次第IPアドレスを取得する
------------------------------"""
def IPaddrget():
	while True:
		try:
			ipaddr = requests.get('http://ifconfig.me/all.json').json()['ip_addr']
		except requests.exceptions.ConnectionError:
			print("インターネット接続待ち…")
			time.sleep(3)
		else:
			break
	return ipaddr


"""------------------------------
LINEで通知を送信する


------------------------------"""
def send_line_notify(line_notify_token,notification_message):
	line_notify_api = 'https://notify-api.line.me/api/notify'
	headers = {'Authorization': f'Bearer {line_notify_token}'}
	data = {'message': notification_message}
	requests.post(line_notify_api, headers = headers, data = data)


"""------------------------------
PCの電源操作

my_function.windows_power_operation('スリープ')

conditionは
再起動、シャットダウン、スリープ、サスペンド
から選べる
------------------------------"""
def windows_power_operation(condition):
	import os
	import ctypes

	if condition=='再起動':
		os.system('shutdown -r -f')
	elif condition=='シャットダウン':
		os.system('shutdown -s -f')
	elif condition=='スリープ':
		ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
	elif condition=='サスペンド':
		ctypes.windll.PowrProf.SetSuspendState(1, 1, 0)


"""------------------------------
DEBUG True 時は全てを表示するが、何も記録しない
DEBUG False 時は全てを記録するが、DEBUG内容は表示しない

# DEBUG=True
DEBUG=False
の追加も必要

# 大体全部
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(processName)s]-[%(filename)s]-[line:%(lineno)s]-[%(funcName)s]-[%(module)s]-[%(name)s]-[%(message)s]'
# DEBUG=True で良さそうな表示内容
str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
# DEBUG=False で良さそうな表示内容
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'

logger.debug('パスワード')
logger.info('予約内容')
logger.warning('予約指定が無いため終了します')
logger.error('見つからなかった要素')
------------------------------"""
def default_logging(DEBUG,log_file_name,str_format_ptn,file_format_ptn):
	import logging
	logger=logging.getLogger(__name__)
	if DEBUG:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.DEBUG)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
	else:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.INFO)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
		file_handler=logging.FileHandler(log_file_name+'.log')
		file_handler.setLevel(logging.DEBUG)
		file_format=logging.Formatter(file_format_ptn)
		file_handler.setFormatter(file_format)
		logger.addHandler(file_handler)
	# 区切りをあらかじめ付加しておく
	logger.debug('------------------------------------------------------------')
	return logger


"""------------------------------
my_function.winsound_beep(回数,周波数,時間)

良さそうなのは
my_function.winsound_beep(3,1500,500)
------------------------------"""
def winsound_beep(n,freq,time):
	for i in range(n):
		winsound.Beep(freq,time)