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
AC_ID_1='43297181'
AC_PW_1='Y2uj4kH9oA'

# 1回で借り入れる金額(万円)
# 2023年2月6日 10000円と入力する仕様に変更されていた
TFA=10000
# 借入を繰り返す回数
loop_time=25
# loop_time=20
# loop_time=6

# 手続き時のスリープ時間
sleep_time=1

# chromedriver.exeのインストール先
CDM_INST=ChromeDriverManager().install()

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
# 処理関数・クラス
# ------------------------------
def main(ac_id,ac_pass,CDM_INST):
	try:
		# 手続き開始
		logger.info(f'selenium起動')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)
		# ウィンドウ最大化
		driver.maximize_window()

		# ログインページ
		url='https://www.kyusai.co.jp/excludes/dmlite/advisors/'
		logger.debug(f'{url} トップページにアクセス')
		driver.get(url)

		# 登録リンクをクリック
		driver.find_element_by_xpath('//*[text()="ご登録はこちら"]').click()

		# while True:
		# 	try:
		# 		driver.find_element_by_xpath('//*[text()="Amazonギフト券"]')
		# 		break
		# 	except:
		# 		time.sleep(1)

		# wait=WebDriverWait(driver,10)
		# wait.until(expected_conditions.text_to_be_present_in_element(driver,"Amazonギフト券"))

		driver.find_element_by_xpath('//*[text()="進む »"]').click()

		driver.find_element_by_xpath('//*[text()="進む »"]').click()







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
		logger.info(f'処理が終了しました。')
		# driver.quit()
		pass

def t01(ac_id,ac_pass,CDM_INST):
	try:
		logger.info(f'selenium起動')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)
		# ウィンドウ最大化
		driver.maximize_window()

		# ウィンドウサイズと位置を取得
		# for i in range(20):
		# 	time.sleep(1)
		# 	print(i)
		# print(f'位置：{driver.get_window_position()}\nサイズ：{driver.get_window_size()}')

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://www.kyusai.co.jp/excludes/dmlite/advisors/'
		logger.debug(f'{url} トップページにアクセス')
		driver.get(url)

		logger.debug(f'登録リンクをクリック')
		driver.find_element_by_xpath('//*[text()="ご登録はこちら"]').click()

		# ウィンドウが小さいとリンクが表示されないのでここで指定
		logger.debug(f'ウィンドウサイズと位置を指定')
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		logger.debug(f'最後のタブをアクティブにする')
		driver.switch_to.window(driver.window_handles[-1])

		logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(driver,30)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"Amazonギフト券"))

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'生年月日入力')
		# 不要だった
		# driver.execute_script("document.getElementsByClassName('hasDatepicker')[0].removeAttribute('readonly')")
		# driver.find_element_by_css_selector(".hasDatepicker").send_keys("12/2000")
		# Select(driver.find_element_by_css_selector("select.ui-datepicker-month")).select_by_visible_text("12")
		# Select(driver.find_element_by_css_selector("ui-datepicker-year")).select_by_visible_text("1990")
		aaa='12/1990'
		driver.execute_script(f"document.getElementsByClassName('hasDatepicker')[0].setAttribute('value','{aaa}')")

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'性別選択')
		aaa='男性'
		driver.find_element_by_xpath(f'//*[text()=\"{aaa}\"]').click()

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'職業選択')
		aaa='その他'
		driver.find_element_by_xpath(f'//*[text()=\"{aaa}\"]').click()

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'参加可否選択')
		driver.find_element_by_xpath(f'//*[text()="はい、参加します"]').click()

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'同意選択')
		# どうやっても同意するを選択できなかったので同意しないを選択して↑を入力した
		driver.find_element_by_xpath(f'//*[text()="同意しません"]').click()
		pyautogui.press('up')

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()

		logger.debug(f'アカウント情報入力')
		# aaa=['匠','村上','asgireffing@across.axis','asgireffing@across.axis','08088881111']
		# for i in range(4):
		# 	driver.execute_script(f"document.getElementsByClassName('input text-input')[{i}].setAttribute('value','{aaa[i]}')")
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[0].setAttribute('value','匠')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[1].setAttribute('value','村上')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[2].setAttribute('value','asgireffing@across.axis')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[3].setAttribute('value','asgireffing@across.axis')"
		)

		logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()


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
# main(AC_ID_1,AC_PW_1,CDM_INST)

t01(AC_ID_1,AC_PW_1,CDM_INST)