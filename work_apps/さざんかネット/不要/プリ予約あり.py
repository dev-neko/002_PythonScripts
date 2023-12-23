import random
import subprocess
import time
from tkinter import messagebox
from bs4 import BeautifulSoup
import pyautogui
import pyperclip
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from my_module import my_function
import xlwings
import poplib
import re
import requests, os,shutil,math,datetime,schedule



# タスクキルしないとブラウザクラッシュする
subprocess.Popen("taskkill /f /im chromedriver.exe")
time.sleep(1)

# ------------------------------
# ウィンドウサイズ・位置設定
# ------------------------------
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--incognito') #シークレットモード
# chrome_options.add_argument('--headless') #ヘッドレスモード
driver=webdriver.Chrome(options=chrome_options)
#要素が見つかるまで指定した時間まで待機
driver.implicitly_wait(10)
driver.maximize_window()


def pre_reselve(driver):
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
	driver.find_element_by_xpath("//*[text()='松ノ木運動場']").click()
	driver.find_element_by_xpath("//*[text()='人工芝庭球場']").click()
	"""
	Select(driver.find_element_by_name("prptyp")).select_by_visible_text("バスケットボール系")
	driver.find_element_by_name('submit').click()
	Select(driver.find_element_by_name("prpcod")).select_by_visible_text("バスケットボール")
	driver.find_element_by_name('submit').click()
	Select(driver.find_element_by_name("rgnide")).select_by_visible_text("すべての地域")
	driver.find_element_by_name('submit').click()
	driver.find_element_by_xpath("//*[text()='上井草スポーツセンター']").click()
	driver.find_element_by_xpath("//*[text()='体育館１／２面']").click()
	"""

	driver.find_element_by_xpath("//*[@value='  次の週  ']").click()


def after_reselve(driver):
	driver.find_element_by_xpath("//*[text()='予約する']").click()
	driver.find_element_by_name('account').send_keys("31273596")
	driver.find_element_by_name('password').send_keys("0727")
	driver.find_element_by_name('submit').click()

	driver.find_element_by_xpath("//*[contains(text(), '3月12日')]").click()

	# driver.find_element_by_xpath("//*[text()='7：00～9：00']").click()
	# driver.find_element_by_xpath("//*[text()='9：00～11：00']").click()
	driver.find_element_by_xpath("//*[text()='11：00～13：00']").click()
	# driver.find_element_by_xpath("//*[text()='13：00～15：00']").click()
	# driver.find_element_by_xpath("//*[text()='15：00～17：00']").click()
	# driver.find_element_by_xpath("//*[text()='17：00～19：00']").click()
	# driver.find_element_by_xpath("//*[text()='19：00～21：00']").click()
	# driver.find_element_by_xpath("//*[text()='21：00～23：00']").click()

	driver.find_element_by_name('tmpmennumpln1').send_keys("1")
	driver.find_element_by_name('submit').click()
	driver.find_element_by_xpath("//*[@value='申し込む']").click()
	driver.find_element_by_xpath("//*[text()='上記内容に同意して次へ進む']").click()

	# 結果確認
	# driver.find_element_by_xpath("//*[contains(text(), '申し訳ございませんが、予約できませんでした。他の方が先に予約しました。')]")




pre_reselve(driver)

# "08:29:59" に 予約する ボタン押してログインしようとしたけど時間外でログイン出来なかった
schedule.every().day.at("08:30:00").do(after_reselve, driver=driver)
# schedule.every().day.at("21:23:00").do(after_reselve, driver=driver)
while True:
	schedule.run_pending()
	time.sleep(0.1)