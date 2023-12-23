import subprocess
import sys
import time
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

# ------------------------------
# Excelから予約情報取得
# ------------------------------
Excel='さざんかねっと.xlsx'
wb=xlwings.Book(Excel)
sht_cancel=wb.sheets['キャンセル予定枠']
sht_account=wb.sheets['アカウント情報など']

# 予約内容を取得
if sht_cancel.range(1,1).value==None:
	print("予約指定が無いため終了します")
	wb.save()
	wb.close()
	sys.exit()
else:
	res_con=sht_cancel.range(sht_cancel.range(1,1).value+1,2).expand('right').value
	print(res_con)

# 予約内容からサイトの情報と同じ形式に変換
res_day=re.sub(r'\(.*?\)','',res_con[2])
print(res_day)
res_time=res_con[3].replace('分','').replace('時','：')
print(res_time)

# アカウント情報を取得
ac_id=int(sht_account.range(2,2).value)
ac_pass=sht_account.range(3,2).value
# print(ac_id,ac_pass)

# LINEトークンを取得
line_notify_token=sht_account.range(9,1).value
# print(line_notify_token)

# Excelを閉じてプロセスキル
wb.save()
wb.close()
xlwings.App().kill()

# キャンセルできる日時か確認
root = tkinter.Tk()
root.withdraw()
mbox_ask = messagebox.askokcancel("", "指定されていない日時の場合はキャンセルできる日時か確認")
if mbox_ask==False: sys.exit()

# ------------------------------
# selenium設定
# ------------------------------
chrome_options=webdriver.ChromeOptions()
# アダプタエラー、自動テスト…、を非表示
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
# chrome_options.add_argument('--headless') #ヘッドレスモード
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
chrome_options.page_load_strategy='none'
driver=webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# ------------------------------
# サイトにアクセスして事前準備
# ------------------------------
perf_start=time.perf_counter()

print('事前手続き中です…')

url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do"
driver.get(url)

driver.find_element_by_xpath("//*[text()='施設空き状況']").click()
driver.find_element_by_xpath("//*[text()='利用目的から選ぶ']").click()
driver.find_element_by_xpath("//*[text()='利用目的名から選択']").click()

Select(driver.find_element_by_name("prptyp")).select_by_visible_text("屋外テニス系")
driver.find_element_by_name('submit').click()
Select(driver.find_element_by_name("prpcod")).select_by_visible_text("テニス（硬式）")
driver.find_element_by_name('submit').click()
Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
driver.find_element_by_name('submit').click()
driver.find_element_by_xpath("//*[text()='"+res_con[0]+"']").click()
driver.find_element_by_xpath("//*[text()='人工芝庭球場']").click()
"""
Select(driver.find_element_by_name("prptyp")).select_by_visible_text("バスケットボール系")
driver.find_element_by_name('submit').click()
Select(driver.find_element_by_name("prpcod")).select_by_visible_text("バスケットボール")
driver.find_element_by_name('submit').click()
Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
driver.find_element_by_name('submit').click()
driver.find_element_by_xpath("//*[text()='"+res_con[0]+"']").click()
driver.find_element_by_xpath("//*[text()='体育館１／２面']").click()
"""

# 該当の日程が表示されるまで 次の週 ボタンを押し続ける
# もし 次の週 ボタンがなくなったら終了
while True:
	if res_day in BeautifulSoup(driver.page_source,'html.parser').text:
		print('事前手続きが完了したため、8時30分まで待機します。')
		break
	else:
		try:
			driver.find_element_by_xpath("//*[@value='  次の週  ']").click()
		except selenium.common.exceptions.NoSuchElementException:
			print("日程の該当が見つからないため終了します。")
			sys.exit()

perf_end=time.perf_counter()
print(f"事前手続き実行時間：{perf_end-perf_start}")

# ------------------------------
# 8時半になったらログインして予約
# ------------------------------
def after_reselve(driver):
	print('8時30分になったため、ログインして予約を開始します。')

	perf_start=time.perf_counter()

	# ページの読み込みで待機する秒数、これ以上経過すると例外発生
	driver.set_page_load_timeout(10)

	serch_str='予約する'
	while True:
		try:
			driver.find_element_by_xpath("//*[text()='予約する']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	driver.find_element_by_name('account').send_keys(ac_id)
	print('ID入力')
	driver.find_element_by_name('password').send_keys(ac_pass)
	print('PASS入力')

	serch_str='ログイン'
	while True:
		try:
			driver.find_element_by_xpath("//*[@value='ログイン']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			res_result=BeautifulSoup(driver.page_source,'html.parser').text
			if '申し訳ございませんが、同一IDでのログイン数が規定数を超えております。' in res_result:
				print('申し訳ございませんが、同一IDでのログイン数が規定数を超えております。')
				driver.quit()
				proc=subprocess.run("taskkill /f /im chromedriver.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
				sys.exit()
			break
		else:
			print(f'{serch_str} が有るので クリック')

	serch_str=res_day
	while True:
		try:
			driver.find_element_by_xpath("//*[contains(text(),'"+res_day+"')]").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	serch_str=res_time
	while True:
		try:
			driver.find_element_by_xpath("//*[text()='"+res_time+"']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	driver.find_element_by_name('tmpmennumpln1').send_keys("1")
	print('人数入力')

	serch_str='次へ'
	while True:
		try:
			driver.find_element_by_xpath("//*[@value='次へ']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	serch_str='申し込む'
	while True:
		try:
			driver.find_element_by_xpath("//*[@value='申し込む']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	serch_str='上記内容に同意して次へ進む'
	while True:
		try:
			driver.find_element_by_xpath("//*[text()='上記内容に同意して次へ進む']").click()
		except selenium.common.exceptions.TimeoutException:
			print(f'{serch_str} をクリックしたらタイムアウトしたので再試行')
		except selenium.common.exceptions.NoSuchElementException:
			print(f'{serch_str} が無いので ブレイク')
			break
		else:
			print(f'{serch_str} が有るので クリック')

	res_result=BeautifulSoup(driver.page_source,'html.parser').text
	# print(res_result)

	result_list=['申し込みを受け付けました。','申し訳ございませんが、予約できませんでした。他の方が先に予約しました。','大変申し訳ありませんが、システム処理中にエラーが発生いたしました。']

	for result in result_list:
		if result in res_result:
			print(result)
			# LINE に通知
			# my_function.send_line_notify(line_notify_token,result)
			break

	perf_end=time.perf_counter()
	print(f"予約手続き実行時間：{perf_end-perf_start}")
	driver.quit()
	proc=subprocess.run("taskkill /f /im chromedriver.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	# my_function.windows_power_operation('スリープ')
	sys.exit()

# ------------------------------
# タイマー設定
# ------------------------------
# after_reselve(driver)

schedule.every().day.at("08:30:00").do(after_reselve, driver=driver)
while True:
	schedule.run_pending()
	time.sleep(0.1)