# ------------------------------
# ライブラリ
# ------------------------------
# 他
import os
import re
import pyautogui
import xlwings
from bs4 import BeautifulSoup
from datetime import datetime
import time
# selenium系
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
# 自作class
import custom_selenium
import mail_rec

# ------------------------------
# 定数
# ------------------------------

DEBUG=True
# DEBUG=False

# IDPass
AC_ID_1='512363088881'
AC_PW_1='501089'

# 手続き時のスリープ時間
SLEEP_TIME=1

CRE_COUNT=50

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
# Excel の初期設定
# ------------------------------
wb=xlwings.Book('登録データ.xlsx')
# シート指定
sht_acdata=wb.sheets['アカウントデータ']
sht_name_jp=wb.sheets['名前_日本語']
# 既にあるメールアカウントの下から追加をする
# 「メールアドレス」の下に何も記載されていないとエラーになるので対応
if sht_acdata.range(2,1).value==None:
	ac_data_str=sht_acdata.range(1,1)
else:
	ac_data_str=sht_acdata.range(1,1).end("down")



# ------------------------------
# 処理関数・クラス
# ------------------------------
def main():
	try:
		mailrec=mail_rec.Mail_Rec(logger,)
		pass
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'タイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'見つからなかった要素\n{err}')
		# ページ内容取得
		# res_result=BeautifulSoup(driver.page_source,'html.parser').text
		# self.logger.warning(f'要素があったはずのページ内容\n{res_result}')
	# その他の予期しないエラー
	except Exception as err:
		logger.error(f'以下の予期しないエラーが発生\n{err}')
	finally:
		logger.info(f'処理が終了しました。')
		# self.driver.quit()
		pass



# ------------------------------
# main
# ------------------------------
main()