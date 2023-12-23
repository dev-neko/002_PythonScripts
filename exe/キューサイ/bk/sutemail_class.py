# ------------------------------
# ライブラリ
# ------------------------------
import re
import time
from selenium.webdriver.common.by import By


# ------------------------------
# 処理関数・クラス
# ------------------------------
class Sutemail_Class():
	def __init__(self,args):
		self.args=args

	# 捨てメアドにログイン
	def login(self,driver):
		self.args.logger.debug(f'ウィンドウサイズと位置を指定')
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページを開く')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ログインフォームを開く')
		driver.find_element_by_id('link_loginform').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'IDとPW入力')
		driver.find_element_by_id('user_number').send_keys(self.args.AC_ID_1)
		driver.find_element_by_id('user_password').send_keys(self.args.AC_PW_1)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'ログイン')
		driver.find_element_by_xpath(f'//*[text()="ログイン"]').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'いいえ')
		driver.find_element_by_id('area-confirm-dialog-button-cancel').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'リロード')
		driver.refresh()

		self.args.logger.debug(f'捨てメアドにログイン完了')

	# 捨てメアドでメールアドレスを1個だけ作成して返す
	def cre_mailaddr(self,driver):
		# url='https://insitesemea.decipherinc.com/survey/selfserve/53b/g022/2201106#$'
		url='https://m.kuku.lu/index.php'
		self.args.logger.debug(f'{url} トップページにアクセス')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'メールアドレスを自動作成')
		driver.find_element_by_id('link_addMailAddrByAuto').click()
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'メールアドレスを取得')
		cre_mailaddr=driver.find_element_by_id('area-newaddress-view-data').text.split('「')[1].split('」')[0]
		time.sleep(self.args.SLEEP_TIME)

		self.args.logger.debug(f'フォームを閉じる')
		driver.find_element_by_id('link_newaddr_close').click()
		time.sleep(self.args.SLEEP_TIME)

		# self.args.logger.debug(f'メールの設定を開く')
		# driver.find_element_by_xpath(f'//*[text()="{cre_mail}"]').click()
		# time.sleep(self.args.SLEEP_TIME)

		# self.args.logger.debug(f'POP3/SMTPの設定を開く')
		# driver.find_element_by_xpath(f'//*[text()="POP3/SMTP"]').click()
		# time.sleep(self.args.SLEEP_TIME)

		# self.args.logger.debug(f'PW取得')
		# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].get_attribute('innerHTML')
		# sss=driver.find_element(By.ID,'area_pop3').find_elements(By.CSS_SELECTOR,".whitebox")[4].find_elements(By.CSS_SELECTOR,"div > div > div > div")[1].text
		# pop3_pw=driver.find_element(By.CSS_SELECTOR,"#area_pop3 > div:nth-child(2) > div:nth-child(5) > div > div:nth-child(1) > div:nth-child(2)").text
		# time.sleep(self.args.SLEEP_TIME)

		# self.args.logger.debug(f'メールの設定を閉じる')
		# driver.find_element(By.ID,'link_addr_close').click()
		# time.sleep(self.args.SLEEP_TIME)

		# self.args.logger.debug(f'メールの設定を閉じる')
		# driver.find_element(By.ID,'link_addr_close').click()
		# time.sleep(self.args.SLEEP_TIME)

		return cre_mailaddr

	# 指定した捨てメアドのメールアドレスでQサイからの本登録リンクが含まれたメールを受信して本登録リンクを返す
	def mail_rec(self,driver,target_addr):
		url='https://m.kuku.lu/recv.php'
		self.args.logger.debug(f'{url} メール受信ページを開く')
		driver.get(url)
		time.sleep(self.args.SLEEP_TIME)

		# メール受信を待機
		while True:
			try:
				aaa=driver.find_element(
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
					driver.refresh()
					self.args.logger.debug(f'1秒待機')
					time.sleep(self.args.SLEEP_TIME)
			except:
				self.args.logger.debug(f'メールが何も届いていないので、1秒待機')
				time.sleep(self.args.SLEEP_TIME)
				pass

		# 最初のiframeがメールの内容なので取得する
		iframe=driver.find_element(By.TAG_NAME,'iframe')
		driver.switch_to.frame(iframe)
		mail_body=driver.find_element(By.CSS_SELECTOR,'#area-data').text
		# print(mail_body)
		# frameを戻す
		# driver.switch_to.frame(iframe)

		# 本登録リンクを抽出する
		reg_link=re.search(r'https.*',mail_body)
		# print(reg_link.group())

		return reg_link.group()