# ------------------------------
# ライブラリ
# ------------------------------
# 他
import re
import time
import sys
import pyautogui
from retry import retry
# selenium系
import selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# ------------------------------
# 処理関数・クラス
# ------------------------------
# 捨てメアド固有のスリープ時間
SUTE_SLEEP_TIME=2

class Sutemail_Class():
	def __init__(self,args,cs):
		self.args=args
		self.driver=cs.sute_driver()
		self.sc_cre_count=0

	# 捨てメアドにログイン
	def login(self):
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページを開く')
		self.driver.get(url)
		# time.sleep(self.args.SLEEP_TIME)
		time.sleep(SUTE_SLEEP_TIME)

		self.args.logger.debug(f'ログインフォームを開く')
		self.driver.find_element_by_id('link_loginform').click()
		# time.sleep(self.args.SLEEP_TIME)
		time.sleep(SUTE_SLEEP_TIME)

		self.args.logger.debug(f'IDとPW入力')
		self.driver.find_element_by_id('user_number').send_keys(self.args.AC_ID_1)
		self.driver.find_element_by_id('user_password').send_keys(self.args.AC_PW_1)
		# time.sleep(self.args.SLEEP_TIME)
		time.sleep(SUTE_SLEEP_TIME)

		self.args.logger.debug(f'ログイン')
		self.driver.find_element_by_xpath(f'//*[text()="ログイン"]').click()
		# time.sleep(self.args.SLEEP_TIME)
		time.sleep(SUTE_SLEEP_TIME)

		self.args.logger.debug(f'いいえ')
		self.driver.find_element_by_id('area-confirm-dialog-button-cancel').click()
		# time.sleep(self.args.SLEEP_TIME)
		time.sleep(SUTE_SLEEP_TIME)

		# リロードするよりトップページを開いた方が安定した
		# self.args.logger.debug(f'リロード')
		# self.driver.refresh()

		# self.args.logger.debug(f'{url} トップページを開く')
		# self.driver.get(url)
		# # time.sleep(self.args.SLEEP_TIME)
		# time.sleep(SUTE_SLEEP_TIME)

		self.args.logger.debug(f'捨てメアドにログイン完了')

	# 捨てメアドでメールアドレスを1個だけ作成して返す
	def cre_mailaddr(self):
		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページにアクセス')
		# たまにここでタイムアウトすることあり
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		# メールアドレスが2千個になってなくても表示されることがあるのでとりあえずOKクリックして続行する
		# 10回繰り返しても先に進めなかったら本当に2千個作成したとして終了する
		for count in range(10):
			self.args.logger.debug(f'メールアドレスを自動作成')
			self.driver.find_element_by_id('link_addMailAddrByAuto').click()
			time.sleep(self.args.SLEEP_TIME)
			# time.sleep(3)

			# メールアドレスが2千個になった場合の処理
			try:
				self.args.logger.debug(f'メールアドレスの最大数の超過警告表示待機')
				WebDriverWait(self.driver,3).until(
					expected_conditions.text_to_be_present_in_element(
						(By.ID,"area-alert-dialog-data"),"メールアドレスの最大数を超過しました。不要なメールアドレスの削除をお願いします。"))
				self.args.logger.debug(f'メールアドレスの最大数の超過警告が表示されたのでOKをクリック')
				self.driver.find_element(By.ID,'area-alert-dialog-button-ok').click()
				time.sleep(self.args.SLEEP_TIME)
				# time.sleep(3)
			except:
				break

			self.args.logger.debug(f'count:{count+1}')
			if count>=9:
				self.args.logger.debug(f'本当にメールアドレスの最大数が超過したのでプログラムを終了')
				sys.exit()

		# アカウント作成後1回のみ利用規約に同意が必要
		# スクリプト初回起動時のみ確認
		# if self.sc_cre_count==0:
		if self.args.CRE_COUNT==0:
			try:
				self.args.logger.debug(f'利用規約同意表示待機')
				WebDriverWait(self.driver,3).until(
					expected_conditions.text_to_be_present_in_element(
						(By.ID,"area-confirm-dialog-data"),"利用規約に同意していただけますか？"))
				self.driver.find_element(By.ID,'area-confirm-dialog-button-ok').click()
				self.args.logger.debug(f'利用規約に同意 はいをクリック')
				# self.sc_cre_count+=1
				time.sleep(self.args.SLEEP_TIME)
			except:
				pass

		cre_mailaddr=self.driver.find_element_by_id('area-newaddress-view-data').text.split('「')[1].split('」')[0]
		# self.args.logger.debug(f'作成したメールアドレス {cre_mailaddr}')
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'フォームを閉じる')
		self.driver.find_element_by_id('link_newaddr_close').click()
		time.sleep(self.args.SLEEP_TIME)

		return cre_mailaddr

	# 指定した捨てメアドのメールアドレス宛のオカネコからの本登録リンクが含まれたメールを受信して本登録リンクをクリックする
	def mail_rec_click(self,target_addr):
		url='https://m.kuku.lu/recv.php'
		self.args.logger.debug(f'{url} メール受信ページを開く')
		self.driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		# メール受信を待機
		while True:
			try:
				mail_hedder=self.driver.find_element(
					By.XPATH,
					'//*[contains(text(),"メールアドレスを認証してください")]/../../..'
				)
				send_addr=mail_hedder.find_element(By.XPATH,"div[2] / div").text
				# print(send_addr)

				if target_addr in send_addr:
					self.args.logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					mail_hedder.click()
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
		# →今回は2番目が先頭メールの内容だった
		iframe=self.driver.find_elements(By.TAG_NAME,'iframe')
		self.driver.switch_to.frame(iframe[1])
		time.sleep(self.args.SLEEP_TIME)

		# click()してリンクを開く
		self.args.logger.debug(f'メールアドレスを認証する')
		self.driver.find_element(By.XPATH,'//*[text()="メールアドレスを認証する"]').click()

		self.args.logger.debug(f'もとのフレームに戻る')
		self.driver.switch_to.default_content()

		self.args.logger.debug(f'オカネコのタブに切り替える')
		self.driver.switch_to.window(self.driver.window_handles[1])

		self.args.logger.debug(f'会員登録が完了しました')
		self.driver.implicitly_wait(30)
		WebDriverWait(self.driver,30).until(
			expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR,"h2"),"会員登録が完了しました"))

		self.args.logger.debug(f'オカネコのタブを閉じる')
		self.driver.close()

		self.args.logger.debug(f'捨てメアドのタブに切り替える')
		self.driver.switch_to.window(self.driver.window_handles[-1])

	# 指定した捨てメアドのメールアドレス宛のオカネコからの本登録リンクが含まれたメールを受信して本登録リンクを返す
	def mail_rec_return_link(self,target_addr):
		url='https://m.kuku.lu/recv.php'
		self.args.logger.debug(f'{url} メール受信ページを開く')
		self.driver.get(url)
		# time.sleep(self.args.SLEEP_TIME)

		# メール受信を待機
		while True:
			try:
				mail_hedder=self.driver.find_element(
					By.XPATH,
					'//*[contains(text(),"メールアドレスを認証してください")]/../../..'
				)
				send_addr=mail_hedder.find_element(By.XPATH,"div[2] / div").text
				# print(send_addr)

				if target_addr in send_addr:
					self.args.logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					mail_hedder.click()
					break
				else:
					self.args.logger.debug(f'リロード')
					self.driver.refresh()
					self.args.logger.debug(f'1秒待機')
					time.sleep(self.args.SLEEP_TIME)
			except:
				self.args.logger.debug(f'メールが何も届いていないのでリロード')
				self.driver.refresh()
				self.args.logger.debug(f'1秒待機')
				time.sleep(self.args.SLEEP_TIME)

		# 最初のiframeがメールの内容なので切り替える
		# →今回は2番目が先頭メールの内容だった
		iframe=self.driver.find_elements(By.TAG_NAME,'iframe')
		self.driver.switch_to.frame(iframe[1])
		# time.sleep(self.args.SLEEP_TIME)

		# 本登録リンクを取得して返す
		reg_link=self.driver.find_element(By.LINK_TEXT,'メールアドレスを認証する').get_attribute('href')
		# print(reg_link)

		return reg_link

	# driverを閉じる
	def quit_driver(self):
		self.args.logger.debug(f'捨てメアドのdriverを閉じる')
		self.driver.quit()
