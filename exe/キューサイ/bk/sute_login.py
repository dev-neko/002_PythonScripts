"""
捨てメアドにログインする
"""

# ------------------------------
# ライブラリ
# ------------------------------
import os

import pyautogui
import xlwings
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
# 処理関数・クラス
# ------------------------------
class Sute_Login():
	def main(self,args,driver):
		args.logger.debug(f'ウィンドウサイズと位置を指定')
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'ログインフォームを開く')
		driver.find_element_by_id('link_loginform').click()
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'IDとPW入力')
		driver.find_element_by_id('user_number').send_keys(args.AC_ID_1)
		driver.find_element_by_id('user_password').send_keys(args.AC_PW_1)
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'ログイン')
		driver.find_element_by_xpath(f'//*[text()="ログイン"]').click()
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'いいえ')
		driver.find_element_by_id('area-confirm-dialog-button-cancel').click()
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'リロード')
		driver.refresh()

		args.logger.debug(f'捨てメアドにログイン完了')