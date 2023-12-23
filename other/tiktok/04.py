import re
import os
import platform
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#Chromeの場所を指定
options = Options()
location = 'C:/Program Files/Google/Chrome Beta/Application/chrome.exe'
options.binary_location = location

#ChromeDriverのヴァージョンを指定
chrome_service = ChromeService(ChromeDriverManager(version='104.0.5112.29').install())
driver = webdriver.Chrome(service=chrome_service,options=options)

#google.comを開く
driver.get('https://google.com')