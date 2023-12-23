# ------------------------------
# ライブラリ
# ------------------------------
# 他
import datetime
import traceback
import click
import xlwings
# selenium系
import selenium
from selenium.common.exceptions import TimeoutException
# 自作class
import custom_selenium,default_logging
import sutemail_class,ac_data_class,okaneko_class


# ------------------------------
# Global定数
# ------------------------------
class Global_Variables():
	DEBUG=True
	# DEBUG=False

	# 手続き時のスリープ時間
	SLEEP_TIME=1

	# logger
	df=default_logging.Default_Logging()
	logger=df.main(DEBUG,'reserve')

	# 使用するプロキシの数
	PROXY_QUANTITY=3

# ------------------------------
# 処理関数・クラス
# ------------------------------
def main(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		# adc=ac_data_class.Ac_Data_Class()
		oc=okaneko_class.Okaneko_Class(args,cs)
		# sc=sutemail_class.Sutemail_Class(args,cs)

		for _ in range(10):
			oc.cre_ac_proxy_test01()

	except selenium.common.exceptions.TimeoutException:
		args.logger.warning(f'タイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		args.logger.warning(f'見つからなかった要素\n{err}')
	# ページ内容取得
	# res_result=BeautifulSoup(driver.page_source,'html.parser').text
	# self.logger.warning(f'要素があったはずのページ内容\n{res_result}')
	except Exception as err:
		args.logger.error(f'以下の予期しないエラーが発生\n{traceback.format_exc()}')
	else:
		args.logger.info(f'処理が正常に終了した')


# ------------------------------
# main
# ------------------------------
args=Global_Variables()

main(args)