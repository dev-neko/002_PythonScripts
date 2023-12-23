"""
記録
2023年2月7日
初期作成
"""

# ------------------------------
# ライブラリ
# ------------------------------
import os

import pyautogui
import xlwings
from bs4 import BeautifulSoup
from datetime import datetime
import time
# selenium系
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# ------------------------------
# 定数
# ------------------------------
DEBUG=True
# DEBUG=False

# IDPass
AC_ID_1='512363088881'
AC_PW_1='501089'

# 手続き時のスリープ時間
SLEEP_TIME=1

# chromedriver.exeのインストール先
CDM_INST=ChromeDriverManager().install()

CRE_COUNT=1

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
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option('detach',True)
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
	# chrome_options.add_argument('--headless')  #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--ignore-certificate-errors')
	# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
	# chrome_options.page_load_strategy='none'
	# 2021年12月30日追加
	# chrome_options.add_argument('--allow-running-insecure-content')
	# chrome_options.add_argument('--disable-web-security')
	# chrome_options.add_argument('--lang=ja')
	# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

	# Herokuではビルドパックが無いと動作しないし、CDM_INSTを指定していても動作しないので、tryで分岐して両対応
	try:
		return webdriver.Chrome(CDM_INST,options=chrome_options)
	except:
		return webdriver.Chrome(options=chrome_options)

# ------------------------------
# Excel の初期設定
# ------------------------------
wb=xlwings.Book('登録データ.xlsx')
# シート指定
sht_acdata=wb.sheets['アカウントデータ']
sht_name_jp=wb.sheets['名前_日本語']
# 既にあるメールアカウントの下から追加をする
# 「メールアドレス」の下に何も記載されていないとエラーになるので対応
if sht_acdata.range(2,1).value==None:
	ac_data_str=sht_acdata.range(1,1)
else:
	ac_data_str=sht_acdata.range(1,1).end("down")

# ------------------------------
# 処理関数・クラス
# ------------------------------
def t01():
	try:
		logger.info(f'selenium起動')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)
		# ウィンドウ最大化
		driver.maximize_window()
		# untilする秒数
		wait=WebDriverWait(driver,30)

		logger.debug(f'ウィンドウサイズと位置を指定')
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/'
		logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(SLEEP_TIME)

		logger.debug(f'ログインフォームを開く')
		driver.find_element_by_id('link_loginform').click()
		time.sleep(SLEEP_TIME)

		logger.debug(f'IDとPW入力')
		driver.find_element_by_id('user_number').send_keys(AC_ID_1)
		driver.find_element_by_id('user_password').send_keys(AC_PW_1)
		time.sleep(SLEEP_TIME)

		logger.debug(f'ログイン')
		driver.find_element_by_xpath(f'//*[text()="ログイン"]').click()
		time.sleep(SLEEP_TIME)

		logger.debug(f'いいえ')
		driver.find_element_by_id('area-confirm-dialog-button-cancel').click()
		time.sleep(SLEEP_TIME)

		logger.debug(f'リロード')
		driver.refresh()

		# 作成回数カウンタ
		CRE_NUM=0
		for i in range(CRE_COUNT):
			# 作成回数カウンタを増やす
			CRE_NUM+=1
			logger.info(f'メールアドレス作成 {CRE_NUM} 回目')

			logger.debug(f'メールアドレスを自動作成')
			driver.find_element_by_id('link_addMailAddrByAuto').click()
			time.sleep(SLEEP_TIME)

			logger.debug(f'メールアドレスを取得')
			cre_mail=driver.find_element_by_id('area-newaddress-view-data').text.split('「')[1].split('」')[0]
			time.sleep(SLEEP_TIME)

			logger.debug(f'フォームを閉じる')
			driver.find_element_by_id('link_newaddr_close').click()
			time.sleep(SLEEP_TIME)

			logger.debug(f'メールの設定を開く')
			driver.find_element_by_xpath(f'//*[text()="{cre_mail}"]').click()
			time.sleep(SLEEP_TIME)

			logger.debug(f'POP3/SMTPの設定を開く')
			driver.find_element_by_xpath(f'//*[text()="POP3/SMTP"]').click()
			time.sleep(SLEEP_TIME)

			logger.debug(f'PW取得')
			# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].get_attribute('innerHTML')
			# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].find_elements(By.CSS_SELECTOR,"div > div > div > div")[1].text
			pop3_pw=driver.find_element(By.CSS_SELECTOR,"#area_pop3 > div:nth-child(2) > div:nth-child(5) > div > div:nth-child(1) > div:nth-child(2)").text
			time.sleep(SLEEP_TIME)

			logger.debug(f'メールの設定を閉じる')
			driver.find_element(By.ID,'link_addr_close').click()
			time.sleep(SLEEP_TIME)

			logger.debug(f'メールの設定を閉じる')
			driver.find_element(By.ID,'link_addr_close').click()
			time.sleep(SLEEP_TIME)







			# 登録データをExcelに記載
			logger.debug(f'メールアドレスを記録 {cre_mail}')
			ac_data_str.offset(CRE_NUM,0).value=cre_mail
			logger.debug(f'POP3PWを記録 {pop3_pw}')
			ac_data_str.offset(CRE_NUM,1).value=pop3_pw





		return
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'タイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		# logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
	# logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理が終了しました。')
		# driver.quit()
		pass

# ------------------------------
# main
# ------------------------------
t01()