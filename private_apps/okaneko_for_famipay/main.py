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

	# メルぽいの、ID、PW
	# AC_ID_1='okaneko_001'
	# AC_PW_1='202195'
	# AC_ID_1='okaneko_002'
	# AC_PW_1='705196'
	# AC_ID_1='okaneko_003'
	# AC_PW_1='599882'
	# AC_ID_1='okaneko_004'
	# AC_PW_1='387595'
	AC_ID_1='okaneko_005'
	AC_PW_1='261095'

	# 手続き時のスリープ時間
	SLEEP_TIME=1

	# 手続きを行う回数
	# CRE_COUNT_DEFAULT=20
	# CRE_COUNT=click.prompt("手続きを行う回数：",type=int,default=CRE_COUNT_DEFAULT)
	# print(CRE_COUNT)
	# CRE_COUNT=2000

	# 申し込み完了日時を取得するために使用
	JST=datetime.timezone(datetime.timedelta(hours=9),'JST')

	# logger
	df=default_logging.Default_Logging()
	logger=df.main(DEBUG,'reserve')

	# 使用するプロキシの数
	PROXY_QUANTITY=3

	# 作成したアカウントの数
	CRE_COUNT=0


	# ------------------------------
	# Excel の初期設定
	# ------------------------------
	wb=xlwings.Book('登録データ.xlsx')
	# シート指定
	sht_acdata=wb.sheets['アカウントデータ']
	# 既にあるメールアカウントの下から追加をする
	# 「メールアドレス」の下に何も記載されていないとエラーになるので対応
	if sht_acdata.range(2,1).value==None:
		ac_data_str=sht_acdata.range(1,1)
	else:
		ac_data_str=sht_acdata.range(1,1).end("down")


# ------------------------------
# 処理関数・クラス
# ------------------------------
def main(args):
	try:
		# インスタンス化
		cs=custom_selenium.Custom_Selenium()
		adc=ac_data_class.Ac_Data_Class()
		oc=okaneko_class.Okaneko_Class(args,cs)
		sc=sutemail_class.Sutemail_Class(args,cs)

		# 捨てメアドにログイン
		sc.login()

		# for cre_count in range(args.CRE_COUNT):
		# cre_count=0
		while True:
			args.logger.debug(f'アカウント作成 {args.CRE_COUNT+1} 回目')
			# args.logger.debug(f'アカウント作成 {cre_count+1} 回目')

			# 捨てメアドでメールアドレスを1個だけ作成して返す
			cre_mailaddr=sc.cre_mailaddr()
			args.logger.debug(f'作成したメールアドレス {cre_mailaddr}')

			# アカウントデータを作成
			ac_data_list,ac_data_dict=adc.cre_data()
			args.logger.debug(f'作成したアカウントデータリスト {ac_data_list}')
			args.logger.debug(f'作成したアカウントデータ辞書 {ac_data_dict}')

			# オカネコのアカウントを作成する
			# 後で同じdriverで操作するためにオカネコのdriverを返す
			okaneko_driver=oc.cre_ac(cre_mailaddr,ac_data_dict)

			# 本登録リンクを取得する
			formal_regist_url=sc.mail_rec_return_link(cre_mailaddr)

			# proxy経由で既に開いているdriverで本登録リンクを開く
			oc.formal_regist(okaneko_driver,formal_regist_url)

			args.logger.debug(f'本登録が完了したアカウントデータをExcelに記載')
			# Excelに記載するデータをリストにまとめる
			ac_data_list.insert(0,cre_mailaddr)
			ac_data_list.append(datetime.datetime.now(args.JST).strftime('%Y/%m/%d(%a) (%p)%I:%M'))
			# Excelに記載する
			args.ac_data_str.offset(args.CRE_COUNT+1).value=ac_data_list
			args.CRE_COUNT+=1
			# args.ac_data_str.offset(cre_count+1).value=ac_data_list
			# cre_count+=1

			# 処理が完了したら捨てメアドのdriverを閉じる
			# if cre_count>=2000:
			# 	sc.quit_driver()
			# 	break

	except selenium.common.exceptions.TimeoutException:
		args.logger.warning(f'タイムアウト')
	except selenium.common.exceptions.NoSuchElementException as err:
		args.logger.warning(f'見つからなかった要素\n{err}')
	# ページ内容取得
	# res_result=BeautifulSoup(driver.page_source,'html.parser').text
	# self.logger.warning(f'要素があったはずのページ内容\n{res_result}')
	except Exception as err:
		args.logger.error(f'以下の予期しないエラーが発生\n{traceback.format_exc()}')
	# else:
	# 	args.logger.info(f'処理が正常に終了した')


# ------------------------------
# main
# ------------------------------
args=Global_Variables()

main(args)