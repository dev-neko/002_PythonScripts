"""
2021年4月23日
8時29分30秒の方がいいかも
2021年4月23日にソース表示されなかったのが気になる
Herokuサーバ起動の待機時間を60秒にした
結果取得のforをelseにした
"""

import subprocess
import sys
import time
import datetime
import tkinter
from tkinter import messagebox
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from my_module import my_function
import xlwings
import re
import schedule
import tkinter
from tkinter import *
from tkinter import font
from my_module import my_function

# DEBUG=True
DEBUG=False

if DEBUG:
	heroku_bd_url="http://127.0.0.1:8000/v1/"
	heroku_ud_url="http://127.0.0.1:8000/userdata/"
else:
	heroku_bd_url="https://sazankanet.herokuapp.com/v1/"
	heroku_ud_url="https://sazankanet.herokuapp.com/userdata/"

heroku_id="Nnp4It3q6A"
heroku_pass="n2Q8rhK49d"

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
# file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]-[%(funcName)s]-[%(module)s]-[%(name)s]\n%(message)s'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
logger=my_function.default_logging(DEBUG,'reserve',str_format_ptn,file_format_ptn)

# ------------------------------
# selenium設定
# ------------------------------
logger.info('ブラウザを起動します。')

chrome_options=webdriver.ChromeOptions()
# アダプタエラー、自動テスト…、を非表示
chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
chrome_options.add_argument('--headless')  #ヘッドレスモード
chrome_options.add_argument('--incognito')  #シークレットモード
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-desktop-notifications')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--user-agent=aheahe')
chrome_options.page_load_strategy='none'  #
driver=webdriver.Chrome(options=chrome_options)

try:
	# ------------------------------
	# Herokuサイトから予約情報取得
	# ------------------------------
	logger.info('ブラウザの起動が完了したため、Herokuサイトより情報を取得します。')

	# サーバがスリープしていると起動に10秒程度必要なので追加
	driver.set_page_load_timeout(60)
	# ページを開いてログイン
	driver.get(heroku_bd_url)
	driver.execute_script('document.getElementById("id_username").value="%s";'%heroku_id)
	logger.debug('ID入力')
	logger.debug(f'heroku_id：{heroku_id}')
	driver.execute_script('document.getElementById("id_password").value="%s";'%heroku_pass)
	logger.debug('PASS入力')
	logger.debug(f'heroku_pass：{heroku_pass}')
	driver.find_element_by_xpath("//button[@type='submit']").click()
	logger.debug('submit')

	# 予約内容を取得
	bs4obj=BeautifulSoup(driver.page_source,'html.parser')
	try:
		res_con=eval(bs4obj.select_one('input[id="reserve_border"]').get('value'))
		logger.info(f'予約内容：{res_con}')
	except:
		logger.warning('予約指定が無いため終了します。')
		sys.exit()

	##########################
	# 確認完了したら削除する #
	##########################
	# res_con=['上井草スポーツセンター','人工芝庭球場Ａ面','4月27日(土)','6時00分～8時00分','4月22日(木)']

	# 予約内容からサイトの情報と同じ形式に変換
	res_day=re.sub(r'\(.*?\)','',res_con[2])
	logger.debug(f'置換した日程：{res_day}')
	res_time=res_con[3].replace('分','').replace('時','：')
	logger.debug(f'置換した時間：{res_time}')

	# さざんかねっとのアカウント情報を取得
	driver.get(heroku_ud_url)
	bs4obj=BeautifulSoup(driver.page_source,'html.parser')
	ac_id=int(bs4obj.select_one('input[name="ac_id"]').get('value'))
	logger.debug(f'Herokuサイトから取得したさざんかねっとID：{ac_id}')
	ac_pass=bs4obj.select_one('input[name="ac_pass"]').get('value')
	logger.debug(f'Herokuサイトから取得したさざんかねっとPASS：{ac_pass}')

	logger.info('Herokuサイトからの情報取得が完了したため、8時29分まで待機します。')

	# ------------------------------
	# サイトにアクセスして事前準備
	# ------------------------------
	def before_reserve():
		perf_start=time.perf_counter()

		logger.info('8時29分になったため、事前手続きを開始します。')

		url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do"
		driver.get(url)

		driver.find_element_by_xpath("//*[text()='施設空き状況']").click()
		logger.debug('施設空き状況')
		driver.find_element_by_xpath("//*[text()='利用目的から選ぶ']").click()
		logger.debug('利用目的から選ぶ')
		driver.find_element_by_xpath("//*[text()='利用目的名から選択']").click()
		logger.debug('利用目的名から選択')

		Select(driver.find_element_by_name("prptyp")).select_by_visible_text("屋外テニス系")
		logger.debug('屋外テニス系')
		driver.find_element_by_name('submit').click()
		logger.debug('submit')
		Select(driver.find_element_by_name("prpcod")).select_by_visible_text("テニス（硬式）")
		logger.debug('テニス（硬式）')
		driver.find_element_by_name('submit').click()
		logger.debug('submit')
		Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
		logger.debug('すべての地域')
		driver.find_element_by_name('submit').click()
		logger.debug('submit')
		driver.find_element_by_xpath("//*[text()='"+res_con[0]+"']").click()
		logger.debug(res_con[0])
		driver.find_element_by_xpath("//*[text()='人工芝庭球場']").click()
		logger.debug('人工芝庭球場')
		"""
				Select(driver.find_element_by_name("prptyp")).select_by_visible_text("バスケットボール系")
				logger.info('バスケットボール系')
				driver.find_element_by_name('submit').click()
				logger.info('submit')
				Select(driver.find_element_by_name("prpcod")).select_by_visible_text("バスケットボール")
				logger.info('バスケットボール')
				driver.find_element_by_name('submit').click()
				logger.info('submit')
				Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
				logger.info('すべての地域')
				driver.find_element_by_name('submit').click()
				logger.info('submit')
				driver.find_element_by_xpath("//*[text()='"+res_con[0]+"']").click()
				logger.info(res_con[0])
				driver.find_element_by_xpath("//*[text()='体育館１／２面']").click()
				logger.info('体育館１／２面')
				"""

		# 該当の日程が表示されるまで 次の週 ボタンを押し続ける
		# もし 次の週 ボタンがなくなったら終了
		while True:
			if res_day in BeautifulSoup(driver.page_source,'html.parser').text:
				logger.info('事前手続きが完了したため、8時30分まで待機します。')
				break
			else:
				try:
					driver.find_element_by_xpath("//*[@value='  次の週  ']").click()
				except selenium.common.exceptions.NoSuchElementException:
					logger.warning("該当の日程が見つからないため終了します。")
					sys.exit()

		perf_end=time.perf_counter()
		logger.info(f"事前手続き実行時間：{perf_end-perf_start}")

	# ------------------------------
	# 8時半になったらログインして予約
	# ------------------------------
	def after_reserve():
		perf_start=time.perf_counter()

		logger.info('8時30分になったため、ログインして予約を開始します。')

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(10)

		try:
			driver.find_element_by_xpath("//*[text()='予約する']").click()
			logger.debug('予約する')
			driver.execute_script('document.getElementsByName("account")[0].value="%s";'%ac_id)
			logger.debug('ID入力')
			driver.execute_script('document.getElementsByName("password")[0].value="%s";'%ac_pass)
			logger.debug('PASS入力')
			driver.find_element_by_xpath("//*[@value='ログイン']").click()
			logger.debug('ログイン')
			driver.find_element_by_xpath("//*[contains(text(),'"+res_day+"')]").click()
			logger.debug(res_day)
			driver.find_element_by_xpath("//*[text()='"+res_time+"']").click()
			logger.debug(res_time)
			driver.execute_script('document.getElementsByName("tmpmennumpln1")[0].value="%s";'%"1")
			logger.debug('人数入力')
			driver.find_element_by_xpath("//*[@value='次へ']").click()
			logger.debug('次へ')
			driver.find_element_by_xpath("//*[@value='申し込む']").click()
			logger.debug('申し込む')
			driver.find_element_by_xpath("//*[text()='上記内容に同意して次へ進む']").click()
			logger.debug('上記内容に同意して次へ進む')
		except selenium.common.exceptions.TimeoutException:
			logger.error(f'タイムアウト')
		except selenium.common.exceptions.NoSuchElementException as err:
			logger.error(f'見つからなかった要素\n{err}')
		finally:
			res_result=BeautifulSoup(driver.page_source,'html.parser').text
			result_list=['申し込みを受け付けました。',
									 '申し訳ございませんが、予約できませんでした。他の方が先に予約しました。',
									 '大変申し訳ありませんが、システム処理中にエラーが発生いたしました。']
			for result in result_list:
				if result in res_result:
					logger.info(result)
					break
			else:
				logger.error(f'エラー発生時のソース\n{res_result}')

			perf_end=time.perf_counter()
			logger.info(f"予約手続き実行時間：{perf_end-perf_start}")

			# 他にもクロドラ使ってたので削除
			# proc=subprocess.run("taskkill /f /im chromedriver.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
			# logger.debug(proc)
			# my_function.windows_power_operation('スリープ')
			logger.info(f'予約手続きが終了しました。')
			sys.exit()

	# ------------------------------
	# タイマー設定
	# ------------------------------
	# before_reserve()
	# after_reserve()

	# schedule.every().day.at("23:17:00").do(before_reserve)
	# schedule.every().day.at("23:18:00").do(after_reserve)

	schedule.every().day.at("08:29:00").do(before_reserve)
	schedule.every().day.at("08:30:00").do(after_reserve)
	while True:
		schedule.run_pending()
		time.sleep(0.1)

except Exception as err:
	logger.error(err)
finally:
	logger.info(f'ブラウザを閉じます。')
	driver.quit()