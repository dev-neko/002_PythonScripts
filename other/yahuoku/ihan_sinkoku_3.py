'''
------------------------------
使い方


------------------------------
更新履歴

前
	ihan_sinkoku_1 だと、読み込みエラーが発生して止まるので
	ihan_sinkoku_2
	はtryとwhileで正常終了するまでループするようにした

2019年8月28日
	auクーポンの場合は出品数が多いので
	ihan_sinkoku_3
	でページにまたがってオークションID取得できるようにした
	------------------------------
	エラーが表示されたときに、forで中断したところから再開できるようにした



------------------------------
'''


import poplib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from my_module import my_function, mail_receiving_pop3
import random
import chromedriver_binary
import time
import openpyxl
import win32com
import xl
import re
import subprocess
import chardet
from my_module import trashmail_mass_production
from selenium.common.exceptions import NoSuchElementException



# ID, PASS
'''
username = 'trashmail_receive_001@yahoo.co.jp'
passwd = 'j50fBU1PvH'
'''
username = 'yutaka_yutakann@yahoo.co.jp'
passwd = 'aQ)|f}lq9ZA4*2670P~>+2KH9(!H92i/'
# 違反申告するオークションID
auk_id = []
# 違反申告するときの開始位置
id_str = 71
# ページのURL
page_url = []



driver = webdriver.Chrome()
driver.set_window_size(1015, 515)

# ヤフオク商品ページに移動
# au クーポン のページ
url = "https://auctions.yahoo.co.jp/search/search?p=au+%E3%82%AF%E3%83%BC%E3%83%9D%E3%83%B3&va=au+%E3%82%AF%E3%83%BC%E3%83%9D%E3%83%B3&exflg=1&b=1&n=100&mode=2&rewrite_category=0"
page_url.append(url)
driver.get(url)
print(my_function.browser_load_wait(driver))

# ページ数取得
# soup.find_all('a', class_= "Pager__link").get("href") は出来ないけど
# 取得したオブジェクト？に.get("href")付ければリンク取得できる
soup = BeautifulSoup(driver.page_source, "html.parser")
for tag in soup.find_all('a', class_= "Pager__link"):
	page_url.append(tag.get("href"))
# 次へ のリンクが最後に入っているので削除
page_url.pop(-1)
print(len(page_url), "ページ")

# オークションID取得
for page_url_fb in page_url:
	driver.get(page_url_fb)
	print(my_function.browser_load_wait(driver))
	soup = BeautifulSoup(driver.page_source, "html.parser")
	for tag in soup.find_all('a', class_= "Product__imageLink"):
		# auction/ から始まって 最後までを切り取り
		tag = re.search('auction\/(.*$)', str(tag.get("href"))).group(1)
		auk_id.append(tag)
print(len(auk_id), "個のオークションを取得")

# ログイン
url = "https://login.yahoo.co.jp/config/login"
driver.get(url)
print(my_function.browser_load_wait(driver))
driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
driver.find_element_by_xpath('//*[@id="btnNext"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="passwd"]').send_keys(passwd)
driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
print(my_function.browser_load_wait(driver))

# 違反申告する
while True:
	try:
		for count, auk_id_fa in enumerate(auk_id[id_str:len(auk_id)]):
			url = "https://auctions.yahoo.co.jp/jp/show/violation_report?aID=" + auk_id_fa
			driver.get(url)
			my_function.browser_load_wait(driver)
			report_soup = BeautifulSoup(driver.page_source, "html.parser")
			if re.search('お客様からの申告状況', str(report_soup)):
				print(count+1, "/", len(auk_id), "自分のオークションなのでスキップ")
				continue
			driver.find_element_by_xpath("//input[@type='radio'][@name='violation_code'][@value='other']").click()
			driver.find_element_by_xpath("//select[@name='other_violation_code']/option[@value='1003']").click()
			driver.find_element_by_xpath("//input[@type='submit'][@value='送信']").click()
			my_function.browser_load_wait(driver)
			print(id_str+count+1, "/", len(auk_id), "の違反申告完了")
	except NoSuchElementException as err:
		print('エラー', err)
		# エラーが表示されたIDから始めるため
		id_str = count
		# driver.quit()
		# time.sleep(1)
		# driver = webdriver.Chrome()
		# driver.set_window_size(1015, 515)
	else:
		break

# 終了処理
print("正常終了")
driver.quit()




