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


# ------------------------------
# ID, PASS
'''
username = 'trashmail_receive_001@yahoo.co.jp'
passwd = 'j50fBU1PvH'
'''
username = 'yutaka_yutakann@yahoo.co.jp'
passwd = 'aQ)|f}lq9ZA4*2670P~>+2KH9(!H92i/'
# 違反申告するオークションIDを入れる
auk_id = []
# ------------------------------
driver = webdriver.Chrome()
driver.set_window_size(1015, 515)
# ------------------------------
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
# ------------------------------
# ヤフオク商品ページに移動
# (ドコモ docomo) (クーポン 割引) -解除 のページ
url = "https://bit.ly/2XWHgrp"
driver.get(url)
print(my_function.browser_load_wait(driver))
# ------------------------------
# オークションID取得
soup = BeautifulSoup(driver.page_source, "html.parser")
for fa, tag in enumerate(soup.find_all('a', class_= "Product__imageLink")):
	# cid: から始まって ; で終わる範囲を切り取り
	tag = re.search('cid:(.*?);', str(tag)).group(1)
	auk_id.append(tag)
print(len(auk_id), "個のオークションを取得")
# ------------------------------
# 違反申告する
for count, fa in enumerate(auk_id):
	url = "https://auctions.yahoo.co.jp/jp/show/violation_report?aID=" + fa
	driver.get(url)
	# print(my_function.browser_load_wait(driver))
	my_function.browser_load_wait(driver)
	report_soup = BeautifulSoup(driver.page_source, "html.parser")
	# ここでシステムエラーになると NoSuchElementException 発生→tryしてurlまで戻りたい
	# for でカウント増やさずに先頭に戻る方法がわからなかった
	if re.search('お客様からの申告状況', str(report_soup)):
		print(count+1, "/", len(auk_id), "自分のオークションなのでスキップ")
		continue
	driver.find_element_by_xpath("//input[@type='radio'][@name='violation_code'][@value='other']").click()
	driver.find_element_by_xpath("//select[@name='other_violation_code']/option[@value='1003']").click()
	driver.find_element_by_xpath("//input[@type='submit'][@value='送信']").click()
	# print(my_function.browser_load_wait(driver))
	my_function.browser_load_wait(driver)
	print(count+1, "/", len(auk_id), "の違反申告完了")
# ------------------------------
# 終了処理
time.sleep(5)
driver.quit()