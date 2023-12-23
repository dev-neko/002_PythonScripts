# ------------------------------
# ライブラリ
# ------------------------------
import os
import pyautogui
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
class Qsai_Class():
	def __init__(self,args,driver):
		self.args=args
		self.driver=driver

	def cre_ac(self,ac_data_dict):
		# ウィンドウ最大化
		self.driver.maximize_window()

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://www.kyusai.co.jp/excludes/dmlite/advisors/'
		self.args.logger.debug(f'{url} トップページにアクセス')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'登録リンクをクリック')
		self.driver.find_element_by_xpath('//*[text()="ご登録はこちら"]').click()
		time.sleep(self.args.SLEEP_TIME)

		# ウィンドウサイズを右半分にする
		self.driver.set_window_size(654,664)
		self.driver.set_window_position(633,0)

		self.args.logger.debug(f'最後のタブをアクティブにする')
		self.driver.switch_to.window(self.driver.window_handles[-1])

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(self.driver,30)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"Amazonギフト券"))

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'生年月日')
		input_value=ac_data_dict['生年月日']
		self.driver.execute_script(
			f"document.getElementsByClassName('hasDatepicker')[0].setAttribute('value','{input_value}')"
		)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'性別')
		input_value=ac_data_dict['性別']
		self.driver.find_element_by_xpath(f'//*[text()=\"{input_value}\"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'職業')
		input_value=ac_data_dict['職業']
		self.driver.find_element_by_xpath(f'//*[text()=\"{input_value}\"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'参加可否選択')
		self.driver.find_element_by_xpath(f'//*[text()="はい、参加します"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'同意選択')
		# どうやっても同意するを選択できなかったので同意しないを選択して↑を入力した
		self.driver.find_element_by_xpath(f'//*[text()="同意しません"]').click()
		pyautogui.press('up')
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'アカウント情報入力')
		# aaa=['匠','村上','asgireffing@across.axis','asgireffing@across.axis','08088881111']
		# for i in range(4):
		# 	self.driver.execute_script(f"document.getElementsByClassName('input text-input')[{i}].setAttribute('value','{aaa[i]}')")
		self.driver.execute_script(
			f"document.getElementsByClassName('input text-input')[0].setAttribute('value',{ac_data_dict['名前']})"
		)
		self.driver.execute_script(
			f"document.getElementsByClassName('input text-input')[1].setAttribute('value',{ac_data_dict['苗字']})"
		)
		self.driver.execute_script(
			f"document.getElementsByClassName('input text-input')[2].setAttribute('value',{ac_data_dict['メールアドレス']})"
		)
		self.driver.execute_script(
			f"document.getElementsByClassName('input text-input')[3].setAttribute('value',{ac_data_dict['メールアドレス']})"
		)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		self.driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ウィンドウを全て閉じる')
		self.driver.quit()