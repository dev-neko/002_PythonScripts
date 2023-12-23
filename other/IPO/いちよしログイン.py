import subprocess
import time
from tkinter import messagebox
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


"""------------------------------
chromeのページ読み込み待ち
------------------------------"""
def browser_load_wait(driver):
	try:
		WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located)
		result = '読込OK ' + driver.title
	except TimeoutException:
		result = "タイムアウト " + driver.title
	except NoSuchElementException:
		result = "エレメントが見つからない " + driver.title
	time.sleep(1)
	return result

# タスクキルしないとブラウザクラッシュする
subprocess.Popen("taskkill /f /im chromedriver.exe")
time.sleep(1)

# ------------------------------
# ウィンドウサイズ・位置設定
# ------------------------------
chrome_options=webdriver.ChromeOptions()
# chrome_options.add_argument('--incognito') #シークレットモード
# chrome_options.add_argument('--headless') #ヘッドレスモード
driver=webdriver.Chrome(options=chrome_options,executable_path=r'C:\Users\YUTANAO\PycharmProjects\PythonScripts\chromedriver.exe')
#要素が見つかるまで指定した最大時間まで待機
driver.implicitly_wait(10)
driver.maximize_window()

url="https://iwas.ichiyoshi.co.jp/ipo/login/direct"
driver.get(url)
print(browser_load_wait(driver))

driver.find_element_by_xpath('//*[@id="customerCd"]').send_keys("136735")
driver.find_element_by_xpath('//*[@id="customerNmKana"]').send_keys("イシダユタカ")
driver.find_element_by_xpath('//*[@id="dateOfBirth"]').send_keys("19900419")
driver.find_element_by_name('submit').click()
print(browser_load_wait(driver))
driver.find_element_by_xpath('//*[@id="ipolist"]').click()

messagebox.showinfo("ナオアカウントに変更")

url="https://iwas.ichiyoshi.co.jp/ipo/login/direct"
driver.get(url)
print(browser_load_wait(driver))

driver.find_element_by_xpath('//*[@id="customerCd"]').send_keys("305472")
driver.find_element_by_xpath('//*[@id="customerNmKana"]').send_keys("プラポンベンチャラット")
driver.find_element_by_xpath('//*[@id="dateOfBirth"]').send_keys("19920404")
driver.find_element_by_name('submit').click()
print(browser_load_wait(driver))
driver.find_element_by_xpath('//*[@id="ipolist"]').click()