"""
捨てメアドでメールアドレスを1個だけ作成する
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
class Cre_Mailaddr():
	def main(self,args,driver):
		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'メールアドレスを自動作成')
		driver.find_element_by_id('link_addMailAddrByAuto').click()
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'メールアドレスを取得')
		cre_mail=driver.find_element_by_id('area-newaddress-view-data').text.split('「')[1].split('」')[0]
		time.sleep(args.SLEEP_TIME)

		args.logger.debug(f'フォームを閉じる')
		driver.find_element_by_id('link_newaddr_close').click()
		time.sleep(args.SLEEP_TIME)

		# args.logger.debug(f'メールの設定を開く')
		# driver.find_element_by_xpath(f'//*[text()="{cre_mail}"]').click()
		# time.sleep(args.SLEEP_TIME)

		# args.logger.debug(f'POP3/SMTPの設定を開く')
		# driver.find_element_by_xpath(f'//*[text()="POP3/SMTP"]').click()
		# time.sleep(args.SLEEP_TIME)

		# args.logger.debug(f'PW取得')
		# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].get_attribute('innerHTML')
		# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].find_elements(By.CSS_SELECTOR,"div > div > div > div")[1].text
		# pop3_pw=driver.find_element(By.CSS_SELECTOR,"#area_pop3 > div:nth-child(2) > div:nth-child(5) > div > div:nth-child(1) > div:nth-child(2)").text
		# time.sleep(args.SLEEP_TIME)

		# args.logger.debug(f'メールの設定を閉じる')
		# driver.find_element(By.ID,'link_addr_close').click()
		# time.sleep(args.SLEEP_TIME)

		# args.logger.debug(f'メールの設定を閉じる')
		# driver.find_element(By.ID,'link_addr_close').click()
		# time.sleep(args.SLEEP_TIME)

		return cre_mail