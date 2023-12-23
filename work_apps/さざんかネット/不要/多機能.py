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

# url="https://www.yoyaku.city.suginami.tokyo.jp/"
# url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/k_index.do" #かんたんフレームなし
url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/p_index.do" #多機能
# url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do " #モバイル
driver.get(url)
print(my_function.browser_load_wait(driver))

# driver.execute_script("chkSubmit()")
driver.execute_script(f"document.getElementsByName(jump(2)).click();")
# driver.find_element_by_link_text('空き情報').click()
