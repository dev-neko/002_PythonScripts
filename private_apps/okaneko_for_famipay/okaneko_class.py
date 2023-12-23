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
import winsound
import pyautogui
# selenium系
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
# 自作class
# import random_class


frequency=500
duration=500


# ------------------------------
# 処理関数・クラス
# ------------------------------
class Okaneko_Class():
	def __init__(self,args,cs):
		self.args=args
		self.cs=cs

	def cre_ac_bk01(self,cre_mailaddr,ac_data_dict):
		driver=self.cs.okaneko_driver()

		# ウィンドウサイズを右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		url='https://okane-kenko.jp/register/email?utm_source=famipay_app&utm_medium=banner&utm_campaign=20231114&redirect=%2Fpartner%2Ffamipay%2Fgettingstarted'
		self.args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		driver.implicitly_wait(60)
		WebDriverWait(driver,60).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h3"),"メールアドレスで登録"))
		driver.implicitly_wait(60)

		self.args.logger.debug(f'ニックネーム {ac_data_dict["ニックネーム"]}')
		driver.find_element(By.NAME,'name').send_keys(ac_data_dict['ニックネーム'])
		self.args.logger.debug(f'メールアドレス {cre_mailaddr}')
		driver.find_element(By.NAME,'email').send_keys(cre_mailaddr)
		self.args.logger.debug(f'PW {ac_data_dict["PW"]}')
		driver.find_element(By.NAME,'password').send_keys(ac_data_dict['PW'])
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'利用規約に同意して登録する')
		# driver.find_element_by_xpath("//*[@value='利用規約に同意して登録する']").click()
		driver.find_element_by_xpath(f'//*[text()="利用規約に同意して登録する"]').click()
		time.sleep(self.args.SLEEP_TIME)

		# ランダムで表示が変わる？
		# 表示内容は関係なかったっぽい
		# self.args.logger.debug(f'指定した文字が表示されるまで待機')
		# wait=WebDriverWait(driver,30)
		# wait.until(
		# 	expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"認証メールを送信しました！") or expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"通信の秘密")
		# )
		# wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"通信の秘密"))

		# self.args.logger.debug(f'オカネコのdriverを閉じる')
		# driver.quit()

		# オカネコのdriverを返して再度操作可能にする
		return driver

	def cre_ac(self,cre_mailaddr,ac_data_dict):
		driver=self.cs.okaneko_driver()

		# ウィンドウサイズを右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# PSOのショートカットでプロキシをランダムに選択する
		# 0～プロキシの数-1の範囲で変更すれば割とランダムに切り替えられそう→プロキシ3個→randint(0,3-1)だと0,1,2→range(2)だと2回
		# 最小化した後だとショートカットキー送れなかった
		pso_sc_count=random.randint(0,self.args.PROXY_QUANTITY-1)
		self.args.logger.debug(f'pso_sc_count:{pso_sc_count}')
		for _ in range(pso_sc_count):
			pyautogui.hotkey('ctrl','shift','o')
			time.sleep(0.5)

		# 最小化
		driver.minimize_window()

		url='https://okane-kenko.jp/register/email?utm_source=famipay_app&utm_medium=banner&utm_campaign=20231114&redirect=%2Fpartner%2Ffamipay%2Fgettingstarted'
		self.args.logger.debug(f'{url} トップページにアクセス')

		# リトライ処理追加
		count=0
		while True:
			try:
				driver.get(url)
				self.args.logger.debug(f'指定した文字が表示されるまで待機')
				# driver.implicitly_wait(60)
				WebDriverWait(driver,60).until(
					expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h3"),"メールアドレスで登録"))
				# driver.implicitly_wait(60)
			except selenium.common.exceptions.TimeoutException:
				self.args.logger.warning(f'タイムアウトしたので再読み込み')
				time.sleep(self.args.SLEEP_TIME)
				# count+=1
				# for _ in range(count):
				# 	winsound.Beep(frequency,duration)
				# 	time.sleep(1)
			else:
				self.args.logger.warning(f'読み込み完了したのでbreak')
				break
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ニックネーム {ac_data_dict["ニックネーム"]}')
		driver.find_element(By.NAME,'name').send_keys(ac_data_dict['ニックネーム'])
		self.args.logger.debug(f'メールアドレス {cre_mailaddr}')
		driver.find_element(By.NAME,'email').send_keys(cre_mailaddr)
		self.args.logger.debug(f'PW {ac_data_dict["PW"]}')
		driver.find_element(By.NAME,'password').send_keys(ac_data_dict['PW'])
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'利用規約に同意して登録する')
		# driver.find_element_by_xpath("//*[@value='利用規約に同意して登録する']").click()
		driver.find_element_by_xpath(f'//*[text()="利用規約に同意して登録する"]').click()
		time.sleep(self.args.SLEEP_TIME)

		# オカネコのdriverを返して再度操作可能にする
		return driver

	def cre_ac_proxy_test01(self):
		driver=self.cs.okaneko_driver()

		# ウィンドウサイズを右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# PSOのショートカットでプロキシをランダムに選択する
		# 0～プロキシの数-1の範囲で変更すれば割とランダムに切り替えられそう→プロキシ3個→randint(0,3-1)だと0,1,2→range(2)だと2回
		pso_sc_count=random.randint(0,self.args.PROXY_QUANTITY-1)
		print(f'pso_sc_count:{pso_sc_count}')
		for _ in range(pso_sc_count):
			pyautogui.hotkey('ctrl','shift','o')

		# url='https://okane-kenko.jp/register/email?utm_source=famipay_app&utm_medium=banner&utm_campaign=20231114&redirect=%2Fpartner%2Ffamipay%2Fgettingstarted'
		url='https://env.b4iine.net/'
		self.args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		time.sleep(3)
		driver.quit()

	# 本登録リンクを開く
	def formal_regist_bk01(self,driver,url):
		self.args.logger.debug(f'{url} 本登録ページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'会員登録が完了しました')
		driver.implicitly_wait(30)
		WebDriverWait(driver,30).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h2"),"会員登録が完了しました"))

		self.args.logger.debug(f'オカネコのdriverを閉じる')
		driver.quit()

	# 本登録リンクを開く
	# リトライ処理追加
	def formal_regist(self,driver,url):
		self.args.logger.debug(f'{url} 本登録ページにアクセス')

		# リトライ処理追加
		while True:
			try:
				driver.get(url)
				self.args.logger.debug(f'指定した文字が表示されるまで待機')
				# driver.implicitly_wait(60)
				WebDriverWait(driver,60).until(
					expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h2"),"会員登録が完了しました"))
			# driver.implicitly_wait(60)
			except selenium.common.exceptions.TimeoutException:
				self.args.logger.warning(f'タイムアウトしたので再読み込み')
				time.sleep(self.args.SLEEP_TIME)
			else:
				self.args.logger.warning(f'読み込み完了したのでbreak')
				break
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'オカネコのdriverを閉じる')
		driver.quit()


class Okaneko_Class_bk01():
	def __init__(self,args,cs):
		self.args=args
		self.driver=cs.okaneko_driver()
		# ウィンドウサイズを右半分にする
		self.driver.set_window_size(654,664)
		self.driver.set_window_position(633,0)

	def cre_ac(self,cre_mailaddr,ac_data_dict):
		url='https://okane-kenko.jp/register/email?utm_source=famipay_app&utm_medium=banner&utm_campaign=20231114&redirect=%2Fpartner%2Ffamipay%2Fgettingstarted'
		self.args.logger.debug(f'{url} トップページにアクセス')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'指定した文字が表示されるまで待機')
		self.driver.implicitly_wait(30)
		WebDriverWait(self.driver,30).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h3"),"メールアドレスで登録"))
		self.driver.implicitly_wait(5)

		self.args.logger.debug(f'ニックネーム {ac_data_dict["ニックネーム"]}')
		self.driver.find_element(By.NAME,'name').send_keys(ac_data_dict['ニックネーム'])
		self.args.logger.debug(f'メールアドレス {cre_mailaddr}')
		self.driver.find_element(By.NAME,'email').send_keys(cre_mailaddr)
		self.args.logger.debug(f'PW {ac_data_dict["PW"]}')
		self.driver.find_element(By.NAME,'password').send_keys(ac_data_dict['PW'])
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'利用規約に同意して登録する')
		# self.driver.find_element_by_xpath("//*[@value='利用規約に同意して登録する']").click()
		self.driver.find_element_by_xpath(f'//*[text()="利用規約に同意して登録する"]').click()
		time.sleep(self.args.SLEEP_TIME)

		# ランダムで表示が変わる？
		# 表示内容は関係なかったっぽい
		# self.args.logger.debug(f'指定した文字が表示されるまで待機')
		# wait=WebDriverWait(driver,30)
		# wait.until(
		# 	expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"認証メールを送信しました！") or expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"通信の秘密")
		# )
		# wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h1"),"通信の秘密"))

		# self.args.logger.debug(f'オカネコのdriverを閉じる')
		# driver.quit()


	def formal_regist(self,url):
		self.args.logger.debug(f'{url} 本登録ページにアクセス')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'会員登録が完了しました')
		self.driver.implicitly_wait(30)
		WebDriverWait(self.driver,30).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h2"),"会員登録が完了しました"))

		self.args.logger.debug(f'オカネコのdriverを閉じる')
		self.driver.quit()
