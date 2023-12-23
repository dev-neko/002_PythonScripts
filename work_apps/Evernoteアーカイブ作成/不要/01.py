# selenium使用


import random
import subprocess
import time
from tkinter import messagebox

import bs4
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
driver=webdriver.Chrome(options=chrome_options,executable_path=r'C:\Users\YUTANAO\PycharmProjects\PythonScripts\chromedriver.exe')
#要素が見つかるまで指定した時間まで待機
driver.implicitly_wait(20)
driver.maximize_window()


def tame01(driver):
	url="https://www.evernote.com/Login.action"
	driver.get(url)

	driver.find_element_by_id('username').send_keys("yutaka_yutakann@yahoo.co.jp")
	driver.find_element_by_id('loginButton').click()
	driver.find_element_by_id('password').send_keys("XB3gWL5J4G")
	driver.find_element_by_id('loginButton').click()

	driver.find_element_by_id('qa-NAV_ALL_NOTEBOOKS').click()

	# driver.find_element_by_xpath("//*[contains(text(), 'ノートブック001')]").click()
	driver.find_element_by_xpath("//*[text()='ノートブック001']").click()

	driver.find_element_by_xpath("//*[text()='≪一発逆転、本気でしたい人はこれに全てをかけて下さい≫']").click()

	# messagebox.showinfo("")

	iframe=driver.find_element_by_tag_name('iframe')
	driver.switch_to.frame(iframe)
	note_obj=BeautifulSoup(driver.page_source,'html.parser')
	note_title_obj=note_obj.find("en-noteheader")
	note_title=note_title_obj.text
	note_conte_obj=note_obj.find("en-note",attrs={'id':'en-note'})
	print(note_conte)

	# html=driver.page_source.encode('utf-8')
	# bs4obj=bs4.BeautifulSoup(html,'html.parser')
	# aaa=bs4obj.find(id="en-note")
	# print(aaa)



tame01(driver)