"""
指定した捨てメアドのメールアドレスで、Qサイからの本登録リンクが含まれたメールを受信する
"""


# ------------------------------
# ライブラリ
# ------------------------------
import re
import time
from selenium.webdriver.common.by import By


# ------------------------------
# 処理関数・クラス
# ------------------------------
class Mail_Rec():
	def main(self,args,driver,target_addr):
		# メール受信ページを開く
		url='https://m.kuku.lu/recv.php'
		args.logger.debug(f'{url} ページにアクセス')
		driver.get(url)
		time.sleep(args.SLEEP_TIME)

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
					args.logger.debug(f'{target_addr} にメールが届いるのでクリックして開く')
					aaa.click()
					break
				else:
					args.logger.debug(f'リロード')
					driver.refresh()
					args.logger.debug(f'1秒待機')
					time.sleep(args.SLEEP_TIME)
			except:
				args.logger.debug(f'メールが何も届いていないので、1秒待機')
				time.sleep(args.SLEEP_TIME)
				pass

		# 最初のiframeがメールの内容なので取得する
		iframe=driver.find_element(By.TAG_NAME,'iframe')
		driver.switch_to.frame(iframe)
		mail_body=driver.find_element(By.CSS_SELECTOR,'#area-data').text
		# print(mail_body)

		# 本登録リンクを抽出する
		reg_link=re.search(r'https.*',mail_body)
		# print(reg_link.group())

		return reg_link.group()