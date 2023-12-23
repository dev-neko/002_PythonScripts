"""
記録
"""

# ------------------------------
# ライブラリ
# ------------------------------
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime
import time

# selenium系
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------
# 定数
# ------------------------------
DEBUG=True
# DEBUG=False

# IDPass
AC_ID_1='dopudopu@xmailer.be'
AC_PW_1='n5tx3(qz0jv~4c'

# 手続き時のスリープ時間
sleep_time=1

# chromedriver.exeのインストール先
# CDM_INST=ChromeDriverManager().install()
# CDM_INST=ChromeDriverManager(version='104.0.5112.20').install()
CDM_INST=ChromeDriverManager(version='104.0.5112.29').install()

# ------------------------------
# logger
# ------------------------------
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

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
logger=default_logging(DEBUG,'reserve',str_format_ptn,file_format_ptn)

# ------------------------------
# selenium
# ------------------------------
def selenium_driver(CDM_INST):
	chrome_options=webdriver.ChromeOptions()
	# Selenium実行終了後もChromeを開いたままにする
	chrome_options.add_experimental_option('detach',True)
	# アダプタエラー、自動テスト…、を非表示
	# chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
	# chrome_options.add_argument('--headless')  #ヘッドレスモード
	# chrome_options.add_argument('--incognito')  #シークレットモード
	# chrome_options.add_argument('--disable-gpu')
	# chrome_options.add_argument('--disable-desktop-notifications')
	# chrome_options.add_argument("--disable-extensions")
	# chrome_options.add_argument('--disable-dev-shm-usage')
	# chrome_options.add_argument('--disable-application-cache')
	# chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument('--ignore-certificate-errors')

	# プロファイルを使用
	# https://engineeeer.com/python-selenium-chrome-login/
	# profile_path=r'C:\Users\YUTAKA\AppData\Local\Google\Chrome\User Data\Default'
	profile_path=r'C:\Users\YUTAKA\AppData\Local\Google\Chrome\User Data\Default\Default'
	chrome_options.add_argument('--user-data-dir=' + profile_path)

	# ↓あまり使わない
	# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
	# chrome_options.page_load_strategy='none'

	# 2021年12月30日追加
	# chrome_options.add_argument('--allow-running-insecure-content')
	# chrome_options.add_argument('--disable-web-security')
	# chrome_options.add_argument('--lang=ja')
	# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

	# Chrome Beta版 を指定
	chrome_options.binary_location='C:/Program Files/Google/Chrome Beta/Application/chrome.exe'

	# return webdriver.Chrome(CDM_INST,options=chrome_options)
	return webdriver.Chrome(service=Service(CDM_INST),options=chrome_options)

# ------------------------------
# 処理関数・クラス
# ------------------------------
def main(ac_id,ac_pass,CDM_INST):
	try:
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)

		# ログインページ
		# url='https://www.tiktok.com/login/phone-or-email/email'
		# driver.get(url)

		url='https://www.tiktok.com'
		driver.get(url)
		time.sleep(sleep_time)

		# url='https://www.tiktok.com/login/qrcode'
		# driver.get(url)

		# driver.find_element_by_xpath("//*[text()='aaa']").click()
		# driver.find_element_by_xpath("//*[contains(text(),'aaa')]").click()

		# driver.find_element_by_xpath("//input[@type='text'][@name='username']").send_keys(ac_id)
		# logger.debug(f'ID入力')
		# driver.find_element_by_xpath("//input[@type='password']").send_keys(ac_pass)
		# logger.debug(f'PASS入力')
		# driver.find_element_by_xpath("//button[@type='submit']").click()
		# logger.debug(f'PASS入力')

		with open('TikTok_Data_1657155605/user_data.json','r',encoding='utf-8') as f:
			json_load = json.load(f)

			for i in json_load["Activity"]["Like List"]["ItemFavoriteList"]:
				url=i["VideoLink"]
				print(url)

				driver.get(url)
				time.sleep(10)

				# webdriver.ActionChains(driver).send_keys("L").perform()








	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'手続き中に60秒間の読み込みが発生してタイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理終了')
		# driver.quit()
		pass

# ------------------------------
# main
# ------------------------------
main(AC_ID_1,AC_PW_1,CDM_INST)