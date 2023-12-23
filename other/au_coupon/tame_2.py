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
from selenium.webdriver.common.alert import Alert
from pykakasi import kakasi



# ------------------------------

# 電話番号取得
for fa in range(5):
	rand_phone = '0' + str(random.randrange(7, 10)) + '0'
	for fb in range(8):
		rand_phone = rand_phone + str(random.randrange(10))
	print(rand_phone)