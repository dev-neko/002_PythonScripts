"""
2度押しはエラーになるので削除した
ヘッドレスでの動作を検討
→オプションをいくつか追加した
8時半以降の処理に対して全体でtryして要素が見つからなければそのソースを表示するように変更
事前手続きもスケジュールして8時29分に実行するようにした
指定されていない日時の場合はキャンセルできるかの確認ウィンドウを表示させた

2021年4月7日
8時30分に予約ボタンクリックしても時間外と表示されたので、クリックする前の時間を表示させた
tk変更
異なる施設に同日同一時間帯の予約があるか確認ウィンドウ追加、
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

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
# file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]-[%(funcName)s]-[%(module)s]-[%(name)s]\n%(message)s'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
logger=my_function.default_logging(DEBUG,'reserve',str_format_ptn,file_format_ptn)

try:

	# ------------------------------
	# Excelから予約情報取得
	# ------------------------------
	Excel='さざんかねっと.xlsx'
	wb=xlwings.Book(Excel)
	sht_cancel=wb.sheets['キャンセル予定枠']
	sht_account=wb.sheets['アカウント情報など']

	# 予約内容を取得
	if sht_cancel.range(1,1).value==None:
		logger.warning('予約指定が無いため終了します。')
		wb.save()
		wb.close()
		xlwings.App().kill()
		sys.exit()
	else:
		res_con=sht_cancel.range(sht_cancel.range(1,1).value+1,2).expand('right').value
		logger.info(f'予約内容：{res_con}')

	# 予約内容からサイトの情報と同じ形式に変換
	res_day=re.sub(r'\(.*?\)','',res_con[2])
	logger.debug(f'置換した日程：{res_day}')
	res_time=res_con[3].replace('分','').replace('時','：')
	logger.debug(f'置換した時間：{res_time}')

	# アカウント情報を取得
	ac_id=int(sht_account.range(2,2).value)
	ac_pass=sht_account.range(3,2).value
	logger.debug(f'Excelから取得したID：{ac_id}')
	logger.debug(f'Excelから取得したPASS：{ac_pass}')

	# LINEトークンを取得
	line_notify_token=sht_account.range(9,1).value
	logger.debug(f'Excelから取得したLINEトークン：{line_notify_token}')

	# Excelを閉じてプロセスキル
	wb.save()
	wb.close()
	xlwings.App().kill()

	# ------------------------------
	# Tkクラスを生成して確認事項を表示する
	# ------------------------------
	'''
	def cre_tkinter(chk_txt):
	
		# Tkクラス生成
		root = Tk()
		# 画面サイズ
		root.geometry()
		root.resizable(False, False)
		# 画面タイトル
		root.title('実行前の確認事項')
	
		# Frameを設定
		frame_label=Frame(root)
		frame_btn=Frame(root)
		# widgetの配置を設定
		padx=10
		pady=5
		frame_label.grid(row=0, column=0, padx=padx, pady=pady)
		frame_btn.grid(row=1, column=0, padx=padx, pady=pady,sticky=(N,S,E,W))
	
		# フォントオブジェクトを新規に作成
		my_font_16=font.Font(root,family='BIZ UDゴシック',size=16)
		my_font_12=font.Font(root,family='BIZ UDゴシック',size=12)
	
		for i in range(len(chk_txt)):
			label = Label(frame_label, text=chk_txt[i], font=my_font_12)
			label.grid(sticky=W)
	
		# ボタン作成
		btn = Button(frame_btn, text="OK", command=root.destroy, font=my_font_12)
		btn.pack(expand=True,fill=tkinter.X,pady=1)
		btn = Button(frame_btn, text="CANCEL", command=sys.exit, font=my_font_12)
		btn.pack(expand=True,fill=tkinter.X,pady=1)
	
		# イベントループ開始
		root.mainloop()
	chk_txt=['・指定されていない日時の場合はキャンセルできる日時か',
					 '・異なる施設に同日同一時間帯の予約はないか',
					 '・予約時間が複数含まれているタイプではないか']
	cre_tkinter(chk_txt)
	'''

	# ------------------------------
	# selenium設定
	# ------------------------------
	logger.info('ブラウザを起動します。')

	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
	chrome_options.add_argument('--headless') #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument('--single-process')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--user-agent=aheahe')
	chrome_options.page_load_strategy='none' #
	driver=webdriver.Chrome(options=chrome_options)
	# driver.maximize_window()

	logger.info('ブラウザの起動が完了したため、8時29分まで待機します。')

	# ------------------------------
	# サイトにアクセスして事前準備
	# ------------------------------
	def before_reselve():
		perf_start=time.perf_counter()

		logger.info('8時29分になったため、事前手続きを開始します。')

		url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do"
		driver.get(url)

		driver.find_element_by_xpath("//*[text()='施設空き状況']").click()
		logger.info('施設空き状況')
		driver.find_element_by_xpath("//*[text()='利用目的から選ぶ']").click()
		logger.info('利用目的から選ぶ')
		driver.find_element_by_xpath("//*[text()='利用目的名から選択']").click()
		logger.info('利用目的名から選択')

		Select(driver.find_element_by_name("prptyp")).select_by_visible_text("屋外テニス系")
		logger.info('屋外テニス系')
		driver.find_element_by_name('submit').click()
		logger.info('submit')
		Select(driver.find_element_by_name("prpcod")).select_by_visible_text("テニス（硬式）")
		logger.info('テニス（硬式）')
		driver.find_element_by_name('submit').click()
		logger.info('submit')
		Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
		logger.info('すべての地域')
		driver.find_element_by_name('submit').click()
		logger.info('submit')
		driver.find_element_by_xpath("//*[text()='"+res_con[0]+"']").click()
		logger.info(res_con[0])
		driver.find_element_by_xpath("//*[text()='人工芝庭球場']").click()
		logger.info('人工芝庭球場')
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
	def after_reselve():
		perf_start=time.perf_counter()

		logger.info('8時30分になったため、ログインして予約を開始します。')

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(10)

		try:
			driver.find_element_by_xpath("//*[text()='予約する']").click()
			logger.info('予約する')
			driver.find_element_by_name('account').send_keys(ac_id)
			logger.info('ID入力')
			driver.find_element_by_name('password').send_keys(ac_pass)
			logger.info('PASS入力')
			driver.find_element_by_xpath("//*[@value='ログイン']").click()
			logger.info('ログイン')
			driver.find_element_by_xpath("//*[contains(text(),'"+res_day+"')]").click()
			logger.info(res_day)
			driver.find_element_by_xpath("//*[text()='"+res_time+"']").click()
			logger.info(res_time)
			driver.find_element_by_name('tmpmennumpln1').send_keys("1")
			logger.info('人数入力')
			driver.find_element_by_xpath("//*[@value='次へ']").click()
			logger.info('次へ')
			driver.find_element_by_xpath("//*[@value='申し込む']").click()
			logger.info('申し込む')
			driver.find_element_by_xpath("//*[text()='上記内容に同意して次へ進む']").click()
			logger.info('上記内容に同意して次へ進む')
		except selenium.common.exceptions.TimeoutException:
			logger.error(f'タイムアウト')
		except selenium.common.exceptions.NoSuchElementException as err:
			logger.error(f'見つからなかった要素\n{err}')
		finally:
			res_result=BeautifulSoup(driver.page_source,'html.parser').text

			result_list=['申し込みを受け付けました。',
									 '申し訳ございませんが、予約できませんでした。他の方が先に予約しました。',
									 '大変申し訳ありませんが、システム処理中にエラーが発生いたしました。']

			result_in=False
			for result in result_list:
				if result in res_result:
					logger.info(result)
					result_in=True
					break
			if result_in==False:
				logger.error(f'エラー発生時のソース\n{res_result}')

			perf_end=time.perf_counter()
			logger.info(f"予約手続き実行時間：{perf_end-perf_start}")

			driver.quit()
			# 他にもクロドラ使ってたので削除
			# proc=subprocess.run("taskkill /f /im chromedriver.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
			# logger.debug(proc)
			# my_function.windows_power_operation('スリープ')
			sys.exit()

	# ------------------------------
	# タイマー設定
	# ------------------------------
	# before_reselve()
	# after_reselve()

	# schedule.every().day.at("23:17:00").do(before_reselve)
	# schedule.every().day.at("23:18:00").do(after_reselve)

	schedule.every().day.at("08:29:00").do(before_reselve)
	schedule.every().day.at("08:30:00").do(after_reselve)
	while True:
		schedule.run_pending()
		time.sleep(0.1)

except Exception as err:
	logger.error(err)