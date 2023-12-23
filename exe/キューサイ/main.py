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
import sutemail_class,qsai_class,ac_data_class

# ------------------------------
# Global定数
# ------------------------------
class Global_Variables():
	DEBUG=True
	# DEBUG=False

	# ID、PW
	AC_ID_1='6107133541'
	AC_PW_1='837600'

	# 手続き時のスリープ時間
	SLEEP_TIME=1

	# 手続きを行う回数
	# CRE_COUNT_DEFAULT=20
	# CRE_COUNT=click.prompt("手続きを行う回数：",type=int,default=CRE_COUNT_DEFAULT)
	# print(CRE_COUNT)
	CRE_COUNT=2000

	# 申し込み完了日時を取得するために使用
	JST=datetime.timezone(datetime.timedelta(hours=9),'JST')

	# logger
	str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
	file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
	df=default_logging.Default_Logging()
	logger=df.main(DEBUG,'reserve',str_format_ptn,file_format_ptn)

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
def main01(args):
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


# ------------------------------
# main
# ------------------------------
args=Global_Variables()

# main01(args)

main02(args)

# test01(args)

# test02(args)