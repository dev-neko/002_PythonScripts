# ------------------------------
# ライブラリ
# ------------------------------
# 他
import re
import time

import pyautogui
from retry import retry
# selenium系
import selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys



# ------------------------------
# 処理関数・クラス
# ------------------------------
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class Sutemail_Class():
	def __init__(self,args,cs):
		self.args=args
		self.driver=cs.sute_driver()

	# 捨てメアドにログイン
	def login(self):
		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページを開く')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ログインフォームを開く')
		self.driver.find_element_by_id('link_loginform').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'IDとPW入力')
		self.driver.find_element_by_id('user_number').send_keys(self.args.AC_ID_1)
		self.driver.find_element_by_id('user_password').send_keys(self.args.AC_PW_1)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ログイン')
		self.driver.find_element_by_xpath(f'//*[text()="ログイン"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'いいえ')
		self.driver.find_element_by_id('area-confirm-dialog-button-cancel').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'リロード')
		self.driver.refresh()

		self.args.logger.debug(f'捨てメアドにログイン完了')

	# 捨てメアドでメールアドレスを1個だけ作成して返す
	def cre_mailaddr(self):
		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページにアクセス')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'メールアドレスを自動作成')
		self.driver.find_element_by_id('link_addMailAddrByAuto').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'メールアドレスを取得')
		cre_mailaddr=self.driver.find_element_by_id('area-newaddress-view-data').text.split('「')[1].split('」')[0]
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'フォームを閉じる')
		self.driver.find_element_by_id('link_newaddr_close').click()
		time.sleep(self.args.SLEEP_TIME)

		return cre_mailaddr

	# 指定した捨てメアドのメールアドレスでQサイからの本登録リンクが含まれたメールを受信して本登録リンクを返す
	def mail_rec(self,target_addr):
		url='https://m.kuku.lu/recv.php'
		self.args.logger.debug(f'{url} メール受信ページを開く')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		# メール受信を待機
		while True:
			try:
				aaa=self.driver.find_element(
					By.XPATH,
					'//*[contains(text(),"ウェルエイジング アドバイザーズに関するあなたのメンバーシップを確認してください")]/../../..'
				)
				send_addr=aaa.find_element(By.XPATH,"div[2] / div").text
				# print(send_addr)

				if target_addr in send_addr:
					self.args.logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					aaa.click()
					break
				else:
					self.args.logger.debug(f'リロード')
					self.driver.refresh()
					self.args.logger.debug(f'1秒待機')
					time.sleep(self.args.SLEEP_TIME)
			except:
				self.args.logger.debug(f'メールが何も届いていないので、1秒待機')
				time.sleep(self.args.SLEEP_TIME)
				pass

		# 最初のiframeがメールの内容なので取得する
		iframe=self.driver.find_element(By.TAG_NAME,'iframe')
		self.driver.switch_to.frame(iframe)
		mail_body=self.driver.find_element(By.CSS_SELECTOR,'#area-data').text
		# print(mail_body)
		# frameを戻す
		# self.driver.switch_to.frame(iframe)

		# 本登録リンクを抽出する
		reg_link=re.search(r'https.*',mail_body)
		# print(reg_link.group())

		return reg_link.group()

	# driverを閉じる
	def quit_driver(self):
		self.args.logger.debug(f'捨てメアドのdriverを閉じる')
		self.driver.quit()

	# 指定した捨てメアドのメールアドレスでQサイからの本登録リンクが含まれたメールを受信して本登録リンクボタンをクリックする
	def mail_rec_click(self,target_addr):
		url='https://m.kuku.lu/recv.php'
		self.args.logger.debug(f'{url} メール受信ページを開く')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		# メール受信を待機
		while True:
			try:
				aaa=self.driver.find_element(
					By.XPATH,
					'//*[contains(text(),"ウェルエイジング アドバイザーズに関するあなたのメンバーシップを確認してください")]/../../..'
				)
				send_addr=aaa.find_element(By.XPATH,"div[2] / div").text
				# print(send_addr)

				if target_addr in send_addr:
					self.args.logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					aaa.click()
					break
				else:
					self.args.logger.debug(f'リロード')
					self.driver.refresh()
					self.args.logger.debug(f'1秒待機')
					time.sleep(self.args.SLEEP_TIME)
			except:
				self.args.logger.debug(f'メールが何も届いていないので、1秒待機')
				time.sleep(self.args.SLEEP_TIME)
				pass

		# 最初のiframeがメールの内容なので切り替える
		iframe=self.driver.find_element(By.TAG_NAME,'iframe')
		self.driver.switch_to.frame(iframe)
		time.sleep(self.args.SLEEP_TIME)

		# .click()できなかったのでENTERを送信してリンクを開く
		self.args.logger.debug(f'アカウント設定を完了する')
		self.driver.find_element(By.XPATH,'//*[text()="アカウント設定を完了する"]').send_keys(Keys.ENTER)

		self.args.logger.debug(f'もとのフレームに戻る')
		self.driver.switch_to.default_content()

		self.args.logger.debug(f'キューサイのタブに切り替える')
		self.driver.switch_to.window(self.driver.window_handles[-1])

		self.args.logger.debug(f'self.driverを返す')
		return self.driver