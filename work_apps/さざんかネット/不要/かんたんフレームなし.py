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
from my_module import my_function
import xlwings
import poplib
import re
import requests
import os
import shutil
import math


# タスクキルしないとブラウザクラッシュする
subprocess.Popen("taskkill /f /im chromedriver.exe")
time.sleep(1)

# ------------------------------
# ウィンドウサイズ・位置設定
# ------------------------------
chrome_options=webdriver.ChromeOptions()
# chrome_options.add_argument('--incognito') #シークレットモード
# chrome_options.add_argument('--headless') #ヘッドレスモード
driver=webdriver.Chrome(options=chrome_options)
#要素が見つかるまで指定した最大時間まで待機
driver.implicitly_wait(10)
driver.maximize_window()

url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/k_index.do"
# url="https://www.yoyaku.city.suginami.tokyo.jp/"
# url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/p_index.do"
# url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/p_TopInitial.do"
driver.get(url)
print(my_function.browser_load_wait(driver))

# ------------------------------
# ログイン
# ------------------------------
driver.find_element_by_xpath("//*[@title='予約や抽選を確認する、または新しく申し込む']").click()
print(my_function.browser_load_wait(driver))
driver.find_element_by_xpath('//*[@id="KEYB3"]').click()
driver.find_element_by_xpath('//*[@id="KEYB1"]').click()
driver.find_element_by_xpath('//*[@id="KEYB2"]').click()
driver.find_element_by_xpath('//*[@id="KEYB7"]').click()
driver.find_element_by_xpath('//*[@id="KEYB3"]').click()
driver.find_element_by_xpath('//*[@id="KEYB5"]').click()
driver.find_element_by_xpath('//*[@id="KEYB9"]').click()
driver.find_element_by_xpath('//*[@id="KEYB6"]').click()
driver.find_element_by_xpath('//*[@id="KEYB0"]').click()
driver.find_element_by_xpath('//*[@id="KEYB7"]').click()
driver.find_element_by_xpath('//*[@id="KEYB2"]').click()
driver.find_element_by_xpath('//*[@id="KEYB7"]').click()
driver.find_element_by_xpath("//*[@title='利用者番号とパスワードを決定する']").click()
# ------------------------------
# 予約 場所指定
# ------------------------------
# driver.find_element_by_xpath("//*[@title='予約の確認、取り消し、または新しく空き施設を探して予約']").click()
# driver.find_element_by_xpath("//*[@title='新しく予約を申し込む']").click()
# driver.find_element_by_xpath("//*[@title='目的で検索']").click()
# driver.find_element_by_xpath("//*[text()='屋外テニス系']").click()
# driver.find_element_by_xpath("//*[text()='テニス（硬式）']").click()
# driver.find_element_by_xpath("//*[@title='すべての地域で検索する']").click()
# driver.find_element_by_xpath("//*[text()='上井草スポーツセンター']").click()
# driver.find_element_by_xpath("//*[text()='人工芝庭球場']").click()

driver.find_element_by_xpath("//*[@title='予約の確認、取り消し、または新しく空き施設を探して予約']").click()
driver.find_element_by_xpath("//*[@title='新しく予約を申し込む']").click()
driver.find_element_by_xpath("//*[@title='目的で検索']").click()
driver.find_element_by_xpath("//*[text()='バドミントン']").click()
driver.find_element_by_xpath("//*[text()='バドミントン']").click()
driver.find_element_by_xpath("//*[@title='すべての地域で検索する']").click()
driver.find_element_by_xpath("//*[text()='上井草スポーツセンター']").click()
driver.find_element_by_xpath("//*[text()='体育館１／６面']").click()
# ------------------------------
# 予約 日時指定
# ------------------------------
driver.find_element_by_xpath("//*[@title='次の一週間を表示']").click()
driver.find_element_by_xpath("//*[@title='次の一週間を表示']").click()
driver.find_element_by_xpath("//*[@title='次の一週間を表示']").click()
driver.find_element_by_xpath("//*[@title='次の一週間を表示']").click()
# 本当は日時を変数にした指定にしたい
driver.find_element_by_xpath('//*[@id="DAY5"]').click()
# driver.find_element_by_xpath("//*[text()='15-17']").click()
driver.find_element_by_xpath("//*[text()='9-11']").click()
driver.find_element_by_xpath("//*[@title='申し込み内容を確認する']").click()
# ------------------------------
# 予約 人数指定
# ------------------------------
driver.find_element_by_xpath("//*[@title='1番目の予約の追加申し込み条件を設定']").click()
driver.find_element_by_xpath("//*[@title='数字1']").click()
driver.find_element_by_xpath("//*[@title='条件を更新する']").click()
driver.find_element_by_xpath("//*[@title='予約を申し込む']").click()
# ------------------------------
# 予約 注意事項確認、予約完了
# ------------------------------
while True:
	try:
		driver.find_element_by_xpath("//*[@class='mCSB_buttonDown']").click()
		driver.find_element_by_xpath("//*[@title='上記内容に同意し次へ進む']").click()
	except selenium.common.exceptions.NoSuchElementException:
		break

# html = driver.page_source.encode('utf-8')
# bs4obj = BeautifulSoup(html,'html.parser')
# print(bs4obj)

# driver.quit()