"""
記録
2023年2月7日
初期作成
"""

# ------------------------------
# ライブラリ
# ------------------------------
# 他
import os
import re
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
# 自作class
import custom_selenium

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

CRE_COUNT=50

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
		sdc=custom_selenium.Custom_Selenium()
		driver=sdc.qsai_driver()

		# ウィンドウ最大化
		driver.maximize_window()
		# untilする秒数
		# wait=WebDriverWait(driver,30)

		# ウィンドウが小さいとリンクが表示されないのでここで指定
		logger.debug(f'ウィンドウサイズと位置を指定')
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/'
		logger.debug(f'{url} ページにアクセス')
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

		# メール受信ページを開く
		url='https://m.kuku.lu/recv.php'
		logger.debug(f'{url} ページにアクセス')
		driver.get(url)
		time.sleep(SLEEP_TIME)

		# メール受信を待機
		target_addr='nyogupa439@mama3.org'
		while True:
			try:
				aaa=driver.find_element(
					By.XPATH,
					'//*[contains(text(),"ウェルエイジング アドバイザーズに関するあなたのメンバーシップを確認してください")]/../../..'
				)
				send_addr=aaa.find_element(By.XPATH,"div[2] / div").text
				# print(send_addr)

				if target_addr in send_addr:
					logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					aaa.click()
					break
				else:
					logger.debug(f'リロード')
					driver.refresh()
					logger.debug(f'1秒待機')
					time.sleep(SLEEP_TIME)
			except:
				logger.debug(f'メールが何も届いていないので、1秒待機')
				time.sleep(SLEEP_TIME)
				pass

		# 最初のiframeがメールの内容なので取得する
		iframe=driver.find_element(By.TAG_NAME,'iframe')
		driver.switch_to.frame(iframe)
		mail_body=driver.find_element(By.CSS_SELECTOR,'#area-data').text
		# print(mail_body)

		# 本登録リンクを抽出する
		reg_link=re.search(r'https.*',mail_body)
		# print(reg_link.group())






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

def t02():
	pass






# ------------------------------
# main
# ------------------------------
t01()
# t02()