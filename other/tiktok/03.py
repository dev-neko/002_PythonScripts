import re
import os
import platform
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#コマンドからインストールされているChromeのヴァージョンを取得
def get_chrome_version(cmd):
	pattern = r'\d+\.\d+\.\d+'
	stdout = os.popen(cmd).read()
	version = re.search(pattern, stdout)
	chrome_version = version.group(0)
	print('Chrome Version : ' + chrome_version)
	return chrome_version

#Chromeのヴァージョンから、適合する最新のChromeDriverのヴァージョンを取得
def get_chrome_driver_version(chrome_version):
	url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + chrome_version
	response = requests.request('GET', url)
	print('ChromeDriver Version : ' + response.text)
	return response.text


#OSを判別
#cmd：それぞれのOSでChrome(Beta)のヴァージョンを確認するコマンド
#location：Chrome(Beta)の場所
pf = platform.system()
if pf == 'Windows':
	print('OS : Windows')
	cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome Beta\BLBeacon" /v version'
	location = 'C:/Program Files/Google/Chrome Beta/Application/chrome.exe'

elif pf == 'Darwin':
	print('OS : Mac')
	cmd = r'/Applications/Google\ Chrome\ Beta.app/Contents/MacOS/Google\ Chrome\ Beta --version'
	location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'

#Chromeのヴァージョン取得
chrome_version = get_chrome_version(cmd)

#Chromeのヴァージョンから、適合する最新のChromeDriverのヴァージョンを取得
driver_version = get_chrome_driver_version(chrome_version)

#Chromeの場所を指定
options = Options()
options.binary_location = location

#ChromeDriverのヴァージョンを指定
chrome_service = ChromeService(ChromeDriverManager(version=driver_version).install())

driver = webdriver.Chrome(service=chrome_service,options=options)

#google.comを開く
driver.get('https://google.com')