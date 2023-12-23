import time
import json

# selenium系
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import configparser



# USER_ID='karupasu1919'
USER_ID='dannasama_'
TIME_SLEEP=5



# driverを返す
def selenium_driver():
	# chromedriver.exeのインストール先
	CDM_INST=ChromeDriverManager().install()
	# 起動時にオプションをつける
	# ポート指定により起動済みのブラウザのドライバーを取得
	chrome_options=webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
	driver=webdriver.Chrome(CDM_INST,options=chrome_options)
	return driver

def main01():
	# 一番右のタブを操作する
	driver.switch_to.window(driver.window_handles[-1])
	driver.refresh()
	time.sleep(TIME_SLEEP)
	while True:
		try:
			if USER_ID not in driver.page_source:
				print(f'配信が開始されていないのでリロード')
				driver.refresh()
			else:
				print(f'配信が開始されたので終了')
				return
		except:
			print(f'エラーが発生したため終了')
			return
		time.sleep(TIME_SLEEP)



driver=selenium_driver()

main01()
# main02()
# main03()