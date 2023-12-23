# ------------------------------
# ライブラリ
# ------------------------------
# 他
import random
import re
import pyautogui
import time
import pyperclip
from retry import retry
# selenium系
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
# 自作class
import random_class

# ------------------------------
# 処理関数・クラス
# ------------------------------
class Qsai_Class():
	def __init__(self,args,cs):
		self.args=args
		self.cs=cs
		self.rc=random_class.Random_Class()

	def cre_ac(self,ac_data_dict):
		driver=self.cs.qsai_driver()

		# ウィンドウ最大化
		driver.maximize_window()

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://www.kyusai.co.jp/excludes/dmlite/advisors/'
		self.args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		driver.implicitly_wait(30)
		WebDriverWait(driver,30).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".text-large"),"ご登録はこちら"))
		driver.implicitly_wait(5)

		self.args.logger.debug(f'登録リンクをクリック')
		driver.find_element_by_xpath('//*[text()="ご登録はこちら"]').click()
		time.sleep(self.args.SLEEP_TIME)

		# ウィンドウサイズを右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		self.args.logger.debug(f'最後のタブをアクティブにする')
		driver.switch_to.window(driver.window_handles[-1])

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(driver,30)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"Amazonギフト券"))

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'生年月日')
		input_value=ac_data_dict['生年月日']
		driver.execute_script(
			f"document.getElementsByClassName('hasDatepicker')[0].setAttribute('value','{input_value}')"
		)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'性別')
		input_value=ac_data_dict['性別']
		driver.find_element_by_xpath(f'//*[text()=\"{input_value}\"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'職業')
		input_value=ac_data_dict['職業']
		driver.find_element_by_xpath(f'//*[text()=\"{input_value}\"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'参加可否選択')
		driver.find_element_by_xpath(f'//*[text()="はい、参加します"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'同意選択')
		# どうやっても同意するを選択できなかったので同意しないを選択して↑を入力した
		driver.find_element_by_xpath(f'//*[text()="同意しません"]').click()
		# time.sleep(self.args.SLEEP_TIME)
		pyautogui.press('up')
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'アカウント情報入力')
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[0].setAttribute('value','{ac_data_dict['名前']}')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[1].setAttribute('value','{ac_data_dict['苗字']}')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[2].setAttribute('value','{ac_data_dict['メールアドレス']}')"
		)
		driver.execute_script(
			f"document.getElementsByClassName('input text-input')[3].setAttribute('value','{ac_data_dict['メールアドレス']}')"
		)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'進む')
		driver.find_element_by_xpath("//*[@value='進む »']").click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(driver,30)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"参加条件の確認が取れ次第"))

		self.args.logger.debug(f'Qサイのウィンドウを全て閉じる')
		driver.quit()

	@retry(exceptions=(selenium.common.exceptions.TimeoutException),tries=10,delay=10)
	def reg_ac_bk01(self,ac_data_dict,reg_link):
		driver=self.cs.qsai_driver()

		# ウィンドウサイズを右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url=reg_link
		self.args.logger.debug(f'{url} 本登録ページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(driver,30)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"アカウントの有効化"))

		self.args.logger.debug(f'ユーザー名')
		regex=re.search(r'(.*)(?=@)',ac_data_dict['メールアドレス'])
		input_value=regex.group()
		driver.find_element(By.NAME,'Username').send_keys(input_value)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'パスワード 1回目')
		driver.find_element(By.NAME,'Password').send_keys(ac_data_dict['QPW'])
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'パスワード 2回目')
		driver.find_element(By.NAME,'ConfirmPassword').send_keys(ac_data_dict['QPW'])
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'有効化を完了')
		driver.find_element_by_xpath('//*[text()="有効化を完了"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		wait=WebDriverWait(driver,10)
		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"ようこそ！"))

		self.args.logger.debug(f'キューサイの仮登録が完了したのでキューサイのdriverを閉じる')
		driver.quit()

	# @retry(exceptions=(selenium.common.exceptions.TimeoutException),tries=2,delay=10)
	def reg_ac(self,ac_data_dict,reg_link):
		while True:
			try:
				self.args.logger.debug(f'reg_link:{reg_link}')
				self.args.logger.debug(f'ac_data_dict:{ac_data_dict}')

				driver=self.cs.qsai_driver()

				# ウィンドウサイズを右半分にする
				# 毎回同じだと怪しいので起動直後のサイズにした、不具合あればサイズと位置をランダムにする
				# driver.set_window_size(654,664)
				# driver.set_window_position(633,0)
				# driver.maximize_window()

				# ウィンドウサイズが1920x1080になったので変更
				# 座標は起動した直後のウィンドウサイズでペイントで手動で求めた、タブとURL欄も考慮済み
				# これより1pxでも小さいと反応しなかった
				posi_offset_x=26
				posi_offset_y=15+120
				# print(f'posi_offset_x:{posi_offset_x}')
				# print(f'posi_offset_y:{posi_offset_y}')
				# print(f'driver.get_window_position():{driver.get_window_position()}')

				url=reg_link
				self.args.logger.debug(f'{url} 本登録ページにアクセス')
				driver.get(url)
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'指定した文字が表示されるまで待機')
				WebDriverWait(driver,30).until(
					expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"アカウントの有効化"))

				self.args.logger.debug(f'ユーザー名')
				regex=re.search(r'(.*)(?=@)',ac_data_dict['メールアドレス'])
				input_value=regex.group()
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'Username'),
					posi_offset_x,
					posi_offset_y,
				)
				pyperclip.copy(input_value)
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'パスワード 1回目')
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'Password'),
					posi_offset_x,
					posi_offset_y,
				)
				pyperclip.copy(ac_data_dict['QPW'])
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				# 要素が見えなくなるので130~200の間でランダムでスクロールする
				scroll_y=random.randint(130,200)
				self.args.logger.debug(f'{scroll_y} px スクロール')
				driver.execute_script(f"window.scrollBy(0,{scroll_y});")
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'パスワード 2回目')
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'ConfirmPassword'),
					posi_offset_x,
					posi_offset_y-scroll_y*1.5, #新PCの倍率分
				)
				pyperclip.copy(ac_data_dict['QPW'])
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'有効化を完了')
				self.rc.pag_random_click(
					driver.find_element_by_xpath('//*[text()="有効化を完了"]'),
					posi_offset_x,
					posi_offset_y-scroll_y*1.5, #新PCの倍率分
				)
				self.args.logger.debug(self.rc.random_sleep())

				# time.sleep(30)
				# return

				self.args.logger.debug(f'指定した文字が表示されるまで待機')
				WebDriverWait(driver,10).until(
					# expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"ようこそ！"))
					expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".page-name"),"ホーム"))
			except selenium.common.exceptions.TimeoutException:
				self.args.logger.warning(f'タイムアウトしたので少し待機してdriverを閉じてやり直す')
				time.sleep(5)
			else:
				self.args.logger.debug(f'キューサイの本登録が完了したのでキューサイのdriverを閉じる')
				break
			finally:
				driver.quit()

	def reg_ac_nolink(self,ac_data_dict,driver):
		# while True:
			try:
				self.args.logger.debug(f'ac_data_dict:{ac_data_dict}')

				# ウィンドウサイズが1920x1080になったので変更
				# 座標は起動した直後のウィンドウサイズでペイントで手動で求めた、タブとURL欄も考慮済み
				# これより1pxでも小さいと反応しなかった
				# posi_offset_x=26
				# posi_offset_y=15+120 #120はタブとURL欄
				posi_offset_x=634*1.5
				posi_offset_y=120
				# print(f'driver.get_window_position():{driver.get_window_position()}')

				# ウィンドウサイズを予め右半分にする
				# driver.set_window_size(654,664)
				# driver.set_window_position(633,0)

				# すぐにリロードするとそれでも表示されないことがあるので少し待つ
				# self.args.logger.debug(self.rc.random_sleep())
				# 足りない時があるのでここだけ個別にランダムに指定
				# random_sec=random.uniform(4,5)
				# self.args.logger.debug(f'{str(random_sec)} 秒間スリープ')
				# time.sleep(random_sec)
				#
				# self.args.logger.debug(f'リロード')
				# driver.refresh()
				#
				# self.args.logger.debug(f'指定した文字が表示されるまで待機')
				# WebDriverWait(driver,30).until(
				# 	expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"アカウントの有効化"))

				while True:
					try:
						self.args.logger.debug(f'指定した文字が表示されるまで待機')
						WebDriverWait(driver,5).until(
							expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"アカウントの有効化"))
					except selenium.common.exceptions.TimeoutException:
						self.args.logger.debug(f'タイムアウトしたのでリロード')
						driver.refresh()
					else:
						break

				self.args.logger.debug(f'ユーザー名')
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'Username'),
					posi_offset_x,
					posi_offset_y,
				)
				pyperclip.copy(ac_data_dict['ユーザー名'])
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				# return

				self.args.logger.debug(f'パスワード 1回目')
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'Password'),
					posi_offset_x,
					posi_offset_y,
				)
				pyperclip.copy(ac_data_dict['QPW'])
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				# 要素が見えなくなるので150~200の間でランダムでスクロールする
				scroll_y=random.randint(150,200)
				self.args.logger.debug(f'{scroll_y} px スクロール')
				driver.execute_script(f"window.scrollBy(0,{scroll_y});")
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'パスワード 2回目')
				self.rc.pag_random_click(
					driver.find_element(By.NAME,'ConfirmPassword'),
					posi_offset_x,
					posi_offset_y-scroll_y*1.5, #新PCの倍率分
				)
				pyperclip.copy(ac_data_dict['QPW'])
				pyautogui.hotkey('ctrl','v')
				self.args.logger.debug(self.rc.random_sleep())

				self.args.logger.debug(f'有効化を完了')
				self.rc.pag_random_click(
					driver.find_element_by_xpath('//*[text()="有効化を完了"]'),
					posi_offset_x,
					posi_offset_y-scroll_y*1.5, #新PCの倍率分
				)
				self.args.logger.debug(self.rc.random_sleep())

				# time.sleep(30)
				# return

				self.args.logger.debug(f'指定した文字が表示されるまで待機')
				driver.implicitly_wait(30)
				WebDriverWait(driver,30).until(
					# expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".title"),"ようこそ！"))
					expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,".page-name"),"ホーム"))
				driver.implicitly_wait(5)
			except selenium.common.exceptions.TimeoutException:
				self.args.logger.warning(f'キューサイの本登録中にタイムアウトした')
				# time.sleep(5)
				raise selenium.common.exceptions.TimeoutException
				# return
			else:
				self.args.logger.debug(f'キューサイの本登録が完了したのでキューサイのタブを閉じる')
				driver.close()
				self.args.logger.debug(f'捨てメアドのタブに切り替える')
				driver.switch_to.window(driver.window_handles[0])
				# break
			finally:
				# driver.quit()
				pass