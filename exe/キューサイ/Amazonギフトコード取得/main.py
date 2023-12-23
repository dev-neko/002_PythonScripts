# ------------------------------
# ライブラリ
# ------------------------------
# 他
import datetime
import traceback
import xlwings
# selenium系
import selenium
from selenium.common.exceptions import TimeoutException
# 自作class
import custom_selenium,default_logging
import sutemail_class

# ------------------------------
# Global定数
# ------------------------------
class Global_Variables():
	DEBUG=True
	# DEBUG=False

	# ID、PW
	AC_IDPW_DIST=[
		{'ID':'266918904631','PW':'280707','CNT':'24','GET':True},# キューサイで手動で申し込む用 24個
		{'ID':'6107133541','PW':'837600','CNT':'163','GET':False},# Pythonでキューサイの申し込みに使用 2つ目 163個
		{'ID':'512363088881','PW':'501089','CNT':'1848','GET':True},# Pythonでキューサイの申し込みに使用 メルアド2千個作成した 1848個
	]

	# 手続き時のスリープ時間
	SLEEP_TIME=1

	# logger
	logger=default_logging.Default_Logging(DEBUG).main()

	# ------------------------------
	# Excel の初期設定
	# ------------------------------
	# ファイル指定
	wb=xlwings.Book('DATA.xlsx')
	# シート指定
	sht_gift=wb.sheets['ギフトカード番号']
	# 途中から再開することはできないので毎回最初から
	sht_gift_str=sht_gift.range(3,2)



# ------------------------------
# 処理関数・クラス
# ------------------------------
def main01(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		sc=sutemail_class.Sutemail_Class(args,cs)

		# 捨てメアドにログイン
		sc.login()

		for cre_count in range(args.CRE_COUNT):
			args.logger.debug(f'アカウント作成 {cre_count+1} 回目')

			# # 捨てメアドでメールアドレスを1個だけ作成して返す
			cre_mailaddr=sc.cre_mailaddr()
			# print(cre_mailaddr)

			# アカウントデータを作成
			# cre_mailaddr='aa@aa.aa'
			ac_data_list,ac_data_dict=adc.cre_data(cre_mailaddr)
			# print(ac_data_list,ac_data_dict)

			# Qサイのアカウントを作成する
			qc.cre_ac(ac_data_dict)

			# # 本登録リンクを取得
			# target_addr='nyogupa439@mama3.org'
			reg_link=sc.mail_rec(cre_mailaddr)
			# print(reg_link)

			# 本登録する
			# reg_link='https://qsaiwellagingadvisers.insitessquare.com/registration/e5e4ea7b-3735-4465-884b-ad1fd776c841'
			# ac_data_dict={'メールアドレス':'gyafayu530@svk.jp','QPW':'S3O2IM2wF8Jf'}
			qc.reg_ac(ac_data_dict,reg_link)

			# 本登録が完了したアカウントデータをExcelに記載
			args.logger.debug(f'本登録が完了したアカウントデータをExcelに記載')
			args.ac_data_str.offset(cre_count+1).value=ac_data_list
			# 申込が完了した日時をExcelに記載
			args.logger.debug(f'申込が完了した日時をExcelに記載')
			args.ac_data_str.offset(cre_count+1,7).value=datetime.datetime.now(args.JST).strftime('%Y/%m/%d(%a) (%p)%I:%M')

		# 処理が完了したら捨てメアドのdriverを閉じる
		sc.quit_driver()

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

def main02(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		adc=ac_data_class.Ac_Data_Class(args)
		qc=qsai_class.Qsai_Class(args,cs)
		sc=sutemail_class.Sutemail_Class(args,cs)

		# 捨てメアドにログイン
		sc.login()

		for cre_count in range(args.CRE_COUNT):
			args.logger.debug(f'アカウント作成 {cre_count+1} 回目')

			# # 捨てメアドでメールアドレスを1個だけ作成して返す
			cre_mailaddr=sc.cre_mailaddr()
			# print(cre_mailaddr)

			# アカウントデータを作成
			# cre_mailaddr='aa@aa.aa'
			ac_data_list,ac_data_dict=adc.cre_data(cre_mailaddr)
			# print(ac_data_list,ac_data_dict)

			# Qサイのアカウントを作成する
			qc.cre_ac(ac_data_dict)

			# 本登録リンクをクリックして新しいタブで開いてその捨てメアドのdriverを返す
			sute_driver=sc.mail_rec_click(cre_mailaddr)

			# 本登録する
			qc.reg_ac_nolink(ac_data_dict,sute_driver)

			# 本登録が完了したアカウントデータをExcelに記載
			args.logger.debug(f'本登録が完了したアカウントデータをExcelに記載')
			args.ac_data_str.offset(cre_count+1).value=ac_data_list
			# 申込が完了した日時をExcelに記載
			args.logger.debug(f'申込が完了した日時をExcelに記載')
			args.ac_data_str.offset(cre_count+1,8).value=datetime.datetime.now(args.JST).strftime('%Y/%m/%d(%a) (%p)%I:%M')

		# 処理が完了したら捨てメアドのdriverを閉じる
		sc.quit_driver()

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

def test01(args):
	try:
		cs=custom_selenium.Custom_Selenium()
		qc=qsai_class.Qsai_Class(args,cs)

		# 本登録する
		reg_link='https://qsaiwellagingadvisers.insitessquare.com/registration/42fcd1ba-6755-43c1-83fe-a529c1b18722'
		ac_data_dict={'メールアドレス':'zekiruta@usako.net','QPW':'S3O2IM2wF8Jf'}
		qc.reg_ac(ac_data_dict,reg_link)

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

def test02(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		sc=sutemail_class.Sutemail_Class(args,cs)
		qc=qsai_class.Qsai_Class(args,cs)

		# 捨てメアドにログイン
		# sc.login()

		# # 本登録リンクを取得
		cre_mailaddr='ribyo@catbar.net'
		sute_driver=sc.mail_rec_click(cre_mailaddr)

		ac_data_dict={'メールアドレス': 'ribyo@catbar.net', 'QPW': 'AyPYN17W1dra', '生年月日': '3/1972', '性別': '男性', '職業': '専門家(医師・弁護士・会計士など)', '苗字': '和田', '名前': '真叶'}
		qc.reg_ac_nolink(ac_data_dict,sute_driver)


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


def test03(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		sc=sutemail_class.Sutemail_Class(args,cs)

		for ac_count,ac in enumerate(args.AC_IDPW_DIST):

			# True→取得する
			if ac['GET']:

				# 捨てメアドにログイン
				sc.login(ac)

				# メールからAmazonギフトコードを取得してリストで返す
				gift_code_list=sc.get_amazon_gift_code(ac)

				args.logger.debug(f'ギフトカード番号のリストをExcelに記載')
				# transpose=Trueで縦に入力
				args.sht_gift_str.offset(0,ac_count).options(transpose=True).value=gift_code_list

				# return

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

# main01(args)

# main02(args)

# test01(args)

test03(args)