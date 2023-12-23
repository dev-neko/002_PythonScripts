"""
記録

2022年5月24日
初期作成

2023年10月30日
第一生命でも同様なCPが開催されたのでプロミスでも対応できるかテスト
"""


# ------------------------------
# ライブラリ
# ------------------------------
import os
from bs4 import BeautifulSoup
from datetime import datetime
import time
# selenium系
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# ------------------------------
# 定数
# ------------------------------
DEBUG=True
# DEBUG=False

# IDPass
AC_ID_1='43297181'
AC_PW_1='Y2uj4kH9oA'
PR_ID_1='rWN7wSy4SIqPSfr78Y3G'
PR_PW_1='hSfQll481gBz736JILAW'

# 1回で借り入れる金額(万円)
# 2023年2月6日 10000円と入力する仕様に変更されていた
TFA=10000
# 借入を繰り返す回数
loop_time=25
# loop_time=23
# loop_time=6

# 手続き時のスリープ時間
sleep_time=1

# chromedriver.exeのインストール先
CDM_INST=ChromeDriverManager().install()


# ------------------------------
# logger
# ------------------------------
def default_logging(DEBUG,log_file_name,str_format_ptn,file_format_ptn):
	import logging
	logger=logging.getLogger(__name__)
	if DEBUG:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.DEBUG)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
	else:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.INFO)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
		file_handler=logging.FileHandler(log_file_name+'.log')
		file_handler.setLevel(logging.DEBUG)
		file_format=logging.Formatter(file_format_ptn)
		file_handler.setFormatter(file_format)
		logger.addHandler(file_handler)
	# 区切りをあらかじめ付加しておく
	logger.debug('------------------------------------------------------------')
	return logger

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
logger=default_logging(DEBUG,'reserve',str_format_ptn,file_format_ptn)


# ------------------------------
# selenium
# ------------------------------
def selenium_driver(CDM_INST):
	chrome_options=webdriver.ChromeOptions()
	# Seleniumでの処理後、Chromeを起動したままにする
	# chrome_options.add_experimental_option('detach',True)
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
	# chrome_options.add_argument('--headless')  #ヘッドレスモード
	# chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--ignore-certificate-errors')

	# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
	# 新しくchromeで取得した
	# USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
	# chrome_options.add_argument(f'--user-agent={USER_AGENT}')

	# chrome_options.page_load_strategy='none'
	# 2021年12月30日追加
	# chrome_options.add_argument('--allow-running-insecure-content')
	# chrome_options.add_argument('--disable-web-security')
	# chrome_options.add_argument('--lang=ja')
	# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

	return webdriver.Chrome(CDM_INST,options=chrome_options)


# ------------------------------
# 処理関数・クラス
# ------------------------------
def main_01(ac_id,ac_pass,CDM_INST):
	try:
		# 手続き開始
		logger.info(f'ログインして振り込み手続きを開始します。')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		# ログインページ
		url='https://www.online-a.com/IbWebp/pc/ac/PALI11.do'
		driver.get(url)
		logger.debug(f'{url} ログインページにアクセス')
		driver.execute_script('document.getElementsByName("memberNo")[0].value="%s";'%ac_id)
		logger.debug(f'ID入力')
		driver.execute_script('document.getElementsByName("pin")[0].value="%s";'%ac_pass)
		logger.debug(f'PASS入力')
		# キーボードから何か入力しないとログインボタンが有効化されない様なので、Xをキーボードから入力してBACKSPACEで消す
		driver.find_element_by_name("pin").send_keys("X")
		driver.find_element_by_name("pin").send_keys(Keys.BACK_SPACE)
		driver.find_element_by_xpath("//*[@value='ログイン']").click()
		logger.debug(f'ログイン')

		# ポイントが付与される上限まで借り入れを繰り返す
		for i in range(loop_time):
			logger.info(f'借り入れ {i+1} 回目')
			# 振り込みで借りるページ
			url='https://www.online-a.com/IbWebp/pc/ac/PAFC01.do'
			driver.get(url)
			logger.debug(f'{url} 振り込みで借りるページにアクセス')
			time.sleep(sleep_time)
			# 振込希望額入力ページ
			url='https://www.online-a.com/IbWebp/pc/ac/PAFC01Branch.do'
			driver.get(url)
			logger.debug(f'{url} 振込希望額入力ページにアクセス')
			time.sleep(sleep_time)
			# 短時間に借り入れると確認ページが表示されるので対応
			try:
				driver.find_element_by_xpath("//*[@value='申込を続ける']").click()
				logger.debug(f'申込を続ける')
				time.sleep(sleep_time)
			except:
				pass
			driver.execute_script('document.getElementsByName("transferAmt")[0].value="%s";'%TFA)
			logger.debug(f'振込希望額 入力')
			time.sleep(sleep_time)
			# 2023年2月6日 追加 str
			driver.find_element_by_name("transferAmt").send_keys(Keys.TAB)
			logger.debug(f'TAB入力')
			time.sleep(sleep_time)
			# 2023年2月6日 追加 end
			driver.find_element_by_xpath("//*[@value='確 認']").click()
			logger.debug(f'確 認')
			time.sleep(sleep_time)
			driver.find_element_by_xpath("//*[@value='送 信']").click()
			logger.debug(f'送 信')
			time.sleep(sleep_time)
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'手続き中に60秒間の読み込みが発生してタイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理が終了しました。')
		# driver.quit()
		pass

# 引数省略、URL遷移ができなくなったのでボタンクリックに変更、
def main_02():
	try:
		# 手続き開始
		logger.info(f'ログインして振り込み手続きを開始します。')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)

		# ログインページ
		url='https://www.online-a.com/IbWebp/pc/ac/PALI11.do'
		driver.get(url)
		logger.debug(f'{url} ログインページにアクセス')
		driver.execute_script('document.getElementsByName("memberNo")[0].value="%s";'%AC_ID_1)
		logger.debug(f'ID入力')
		driver.execute_script('document.getElementsByName("pin")[0].value="%s";'%AC_PW_1)
		logger.debug(f'PASS入力')
		# キーボードから何か入力しないとログインボタンが有効化されない様なので、Xをキーボードから入力してBACKSPACEで消す
		driver.find_element_by_name("pin").send_keys("X")
		driver.find_element_by_name("pin").send_keys(Keys.BACK_SPACE)
		driver.find_element_by_xpath("//*[@value='ログイン']").click()
		logger.debug(f'ログイン')

		# ポイントが付与される上限まで借り入れを繰り返す
		for i in range(loop_time):
			logger.info(f'借り入れ {i+1} 回目')

			# 振り込みで借りるページ
			url='https://www.online-a.com/IbWebp/pc/ac/PAFC01.do'
			driver.get(url)
			logger.debug(f'{url} 振り込みで借りるページにアクセス')
			time.sleep(sleep_time)

			# containsとtext()…で「へ進む」を指定してもクリックできなかったのでcontainsと@valueで部分一致
			driver.find_element(By.XPATH,'//*[contains(@value,"へ進む")]').click()
			logger.debug(f'"振込で借りる"へ進む')
			time.sleep(sleep_time)

			# 短時間に借り入れると確認ページが表示されるので対応
			try:
				driver.find_element_by_xpath("//*[@value='申込を続ける']").click()
				logger.debug(f'申込を続ける')
				time.sleep(sleep_time)
			except:
				pass

			# 下記のお申し込みを受付中です に対応
			try:
				driver.find_element_by_xpath("//*[text()='追加で申し込む']").click()
				logger.debug(f'追加で申し込む')
				time.sleep(sleep_time)
			except:
				pass

			driver.execute_script('document.getElementsByName("transferAmt")[0].value="%s";'%TFA)
			logger.debug(f'振込希望額 入力')
			time.sleep(sleep_time)
			# 振込希望額を入力しただけではボタンが押せないのでtabを入力
			driver.find_element_by_name("transferAmt").send_keys(Keys.TAB)
			logger.debug(f'TAB入力')
			time.sleep(sleep_time)
			driver.find_element_by_xpath("//*[@value='確認する']").click()
			logger.debug(f'確認する')
			time.sleep(sleep_time)
			driver.find_element_by_xpath("//*[@value='申し込む']").click()
			logger.debug(f'申し込む')
			time.sleep(sleep_time)
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'手続き中に60秒間の読み込みが発生してタイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理が終了しました。')
		# driver.quit()
		pass

# 第一生命支店も同CP開催されたので、プロミスの操作ができるかテスト
def main_td_01():
	try:
		# 手続き開始
		logger.info(f'ログインして振り込み手続き開始')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)

		# ログインページ
		url='https://cyber.promise.co.jp/CPA01X/CPA01X01'
		driver.get(url)
		logger.debug(f'{url} ログインページにアクセス')
		#ウィンドウの最大化
		driver.maximize_window()

		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		print(res_result)

		return

		# driver.execute_script('document.getElementsByName("InputWebId")[1].value="%s";'%PR_ID_1)
		# driver.find_elements(By.XPATH,'//input[@type="text"]')[1].send_keys("abcde")
		# driver.execute_script(
		# 	f"document.getElementsByName('InputWebId')[0].setAttribute('value','{PR_ID_1}')"
		# )
		driver.find_element(By.NAME,'InputWebId').send_keys(PR_ID_1)
		print(driver.find_element(By.NAME,'InputWebId'))


		logger.debug(f'ID入力')
		driver.execute_script('document.getElementsByName("ion-input-6")[0].value="%s";'%PR_PW_1)
		logger.debug(f'PASS入力')
		# キーボードから何か入力しないとログインボタンが有効化されない様なので、Xをキーボードから入力してBACKSPACEで消す
		# driver.find_element_by_name("pin").send_keys("X")
		# driver.find_element_by_name("pin").send_keys(Keys.BACK_SPACE)
		driver.find_element_by_xpath("//*[@value='ログイン']").click()
		logger.debug(f'ログイン')

		# ポイントが付与される上限まで借り入れを繰り返す
		for i in range(loop_time):
			logger.info(f'借り入れ {i+1} 回目')

			# 振り込みで借りるページ
			url='https://www.online-a.com/IbWebp/pc/ac/PAFC01.do'
			driver.get(url)
			logger.debug(f'{url} 振り込みで借りるページにアクセス')
			time.sleep(sleep_time)

			# containsとtext()…で「へ進む」を指定してもクリックできなかったのでcontainsと@valueで部分一致
			driver.find_element(By.XPATH,'//*[contains(@value,"へ進む")]').click()
			logger.debug(f'"振込で借りる"へ進む')
			time.sleep(sleep_time)

			# 短時間に借り入れると確認ページが表示されるので対応
			try:
				driver.find_element_by_xpath("//*[@value='申込を続ける']").click()
				logger.debug(f'申込を続ける')
				time.sleep(sleep_time)
			except:
				pass

			# 下記のお申し込みを受付中です に対応
			try:
				driver.find_element_by_xpath("//*[text()='追加で申し込む']").click()
				logger.debug(f'追加で申し込む')
				time.sleep(sleep_time)
			except:
				pass

			driver.execute_script('document.getElementsByName("transferAmt")[0].value="%s";'%TFA)
			logger.debug(f'振込希望額 入力')
			time.sleep(sleep_time)
			# 振込希望額を入力しただけではボタンが押せないのでtabを入力
			driver.find_element_by_name("transferAmt").send_keys(Keys.TAB)
			logger.debug(f'TAB入力')
			time.sleep(sleep_time)
			driver.find_element_by_xpath("//*[@value='確認する']").click()
			logger.debug(f'確認する')
			time.sleep(sleep_time)
			driver.find_element_by_xpath("//*[@value='申し込む']").click()
			logger.debug(f'申し込む')
			time.sleep(sleep_time)
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'手続き中に60秒間の読み込みが発生してタイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理が終了しました。')
		# driver.quit()
		pass

# ------------------------------
# main
# ------------------------------
# main_01(AC_ID_1,AC_PW_1,CDM_INST)
# main_02()
main_td_01()