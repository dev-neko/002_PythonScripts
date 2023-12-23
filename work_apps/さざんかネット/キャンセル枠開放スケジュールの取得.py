import pprint
import subprocess
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from my_module import my_function
import xlwings
import re

# DEBUG=True
DEBUG=False

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]-[%(message)s]'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]-[%(funcName)s]-[%(module)s]-[%(name)s]\n%(message)s'
logger=my_function.default_logging(DEBUG,'get',str_format_ptn,file_format_ptn)

try:
	def get_excel_parser(excel_contents):
		ex_str="\n"
		for i in excel_contents:
			for count,n in enumerate(i):
				if count==len(i)-1:
					ex_str=ex_str+"開放予定日："+n+"\n"
				else:
					ex_str=ex_str+n+"\n"
			ex_str=ex_str+"\n"
		ex_str=ex_str.rstrip("\n")
		return ex_str

	tmp_list=[]
	excel_list=[]

	# ------------------------------
	# ブラウザ起動・設定
	# ------------------------------
	# 予めプロセスキル
	# 他にもクロドラ使ってたので削除
	# proc=subprocess.run("taskkill /f /im chromedriver.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	# logger.debug(proc)
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
	#要素が見つかるまで指定した時間まで待機
	driver.implicitly_wait(10)

	# ------------------------------
	# 情報取得
	# ------------------------------
	url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do"
	driver.get(url)
	driver.find_element_by_xpath("//*[text()='開放予定の案内']").click()
	Select(driver.find_element_by_name("prptyp")).select_by_visible_text("屋外テニス系")
	driver.find_element_by_name('submit').click()
	Select(driver.find_element_by_name("prpcod")).select_by_visible_text("テニス（硬式）")
	driver.find_element_by_name('submit').click()
	# 内容取得・整理
	while True:
		bs4obj=BeautifulSoup(driver.page_source,'html.parser')
		cb_data=bs4obj.find("form",attrs={'name':'searchObjForm'}).text.split()
		for count,i in enumerate(cb_data):
			if count>5 and i not in "次前" and i not in "[開放予定日]":
				tmp_list.append(re.sub(r'[◇・\s]','',i))
				if (count-5)%6==0:
					excel_list.append(tmp_list)
					tmp_list=[]
		try:
			driver.find_element_by_xpath("//*[text()='次']").click()
		except selenium.common.exceptions.NoSuchElementException:
			break
	driver.quit()

	logger.debug(f'オリジナルの取得した内容\n{excel_list}')

	# 9時00分～19時00分 が含まれていた場合は5つの時間帯に修正
	except_time_list=['9時00分～11時00分','11時00分～13時00分','13時00分～15時00分','15時00分～17時00分','17時00分～19時00分']
	for c1,i in enumerate(excel_list):
		if '9時00分～19時00分' in i[3]:
			for c2,except_time in enumerate(except_time_list):
				excel_list[c1+c2][3]=except_time
			break

	logger.info(f'取得した内容\n{excel_list}')

	# ------------------------------
	# Excelに書き込み・保存
	# ------------------------------
	Excel='さざんかねっと.xlsx'
	wb=xlwings.Book(Excel)
	sht_cancel=wb.sheets['キャンセル予定枠']
	sht_account=wb.sheets['アカウント情報など']

	# 内容初期化
	sht_cancel.range(2,2).expand('table').clear_contents()
	# ラジオボタンの選択解除
	sht_cancel.range(1,1).clear_contents()
	# 書き込み
	sht_cancel.range(2,2).value=excel_list

	# LINEとメールの通知用に整理した内容を取得
	excel_parser=get_excel_parser(sht_cancel.range(2,2).expand('table').value)
	# print(excel_parser)
	line_notify_token=sht_account.range(9,1).value
	logger.debug(f'Excelから取得したLINEトークン：{line_notify_token}')
	to_email=sht_account.range(6,1).value
	logger.debug(f'Excelから取得したメールアドレス：{to_email}')

	wb.save()
	# wb.close()
	# xlwings.App().kill()

	# ------------------------------
	# LINE・メールアドレス に通知
	# ------------------------------
	# LINE に通知
	my_function.send_line_notify(line_notify_token,excel_parser)
	# メールアドレス に通知
	subject='さざんかねっと キャンセル枠開放スケジュール'
	my_function.outlook_mail_send_smtp_starttls(to_email,subject,excel_parser)
except Exception as err:
	logger.error(err)