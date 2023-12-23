'''
トラメで1回だけ受信可能なメルアドを作成する
無料版は25個までしかメル作れないけど、1回受信してメル消せばいくつも作れる

戻り値
作成したメルアド

使い方
from my_module import trashmail_mass_production

driver = webdriver.Chrome()
driver.set_window_size(1015, 515)
trans_mail = 'trashmail_receive_001@yahoo.co.jp'
create_mail = trashmail_mass_production.create_mail(driver, trans_mail)

注意
メルアド作成するとトラメから作成した旨のメルが届くので受信拒否するかフォルダに分ける
→件名でフィルタリングしたので不要
'''
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from my_module import my_function
import random
import time

def create_mail(driver, trans_mail):
	tram_domain = [
		"0box.eu",
		"contbay.com",
		"damnthespam.com",
		"kurzepost.de",
		"objectmail.com",
		"proxymail.eu",
		"rcpt.at",
		"trash-mail.at",
		"trashmail.at",
		"trashmail.com",
		"trashmail.io",
		"trashmail.me",
		"trashmail.net",
		"wegwerfmail.de",
		"wegwerfmail.net",
		"wegwerfmail.org"
		]

	driver.get("https://trashmail.com")
	print(my_function.browser_load_wait(driver))

	while True:
		try:
			# トラメが決めた表示されているアカウント名を取得
			mail_name = driver.find_element_by_xpath('//*[@id="fe-mob-name"]').get_attribute("value")
			time.sleep(0.5)
			print('読込OK ' + driver.title)
			break
		except NoSuchElementException:
			print("エレメント見つからない " + driver.title)

	# ドメインを選択
	element = driver.find_element_by_xpath('//*[@id="fe-mob-domain"]')
	domain_num = random.randrange(len(tram_domain))
	Select(element).select_by_value(tram_domain[domain_num])
	time.sleep(0.5)

	# 転送先メルアドを入力
	driver.find_element_by_xpath('//*[@id="fe-mob-forward"]').send_keys(trans_mail)
	time.sleep(0.5)

	# 転送回数を選択
	element = driver.find_element_by_xpath('//*[@id="fe-mob-fwd-nb"]')
	Select(element).select_by_value('1')
	time.sleep(0.5)

	# 利用期間を選択
	element = driver.find_element_by_xpath('//*[@id="fe-mob-life-span"]')
	Select(element).select_by_value('31')
	time.sleep(0.5)

	# Disable CAPTCHA system を選択
	driver.find_element_by_xpath('//*[@id="tab-mob-quick"]/form/div[5]/div[2]/label').click()

	# Notify me when my account has expired. のチェックを外す
	driver.find_element_by_xpath('//*[@id="tab-mob-quick"]/form/div[5]/div[3]/label').click()

	# createボタンを押す
	driver.find_element_by_xpath('//*[@id="fe-mob-submit"]').click()
	print(my_function.browser_load_wait(driver))

	cre_mail = mail_name + '@' + tram_domain[domain_num]
	print(cre_mail)

	return cre_mail
