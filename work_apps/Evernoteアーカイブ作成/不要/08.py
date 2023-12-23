# GoogleドキュメントAPI検証用



def note_title_get_from_gspread(JSON_KEYFILE_NAME,SPREADSHEET_KEY,SPREADSHEET_NAME):

	import datetime
	import gspread

	#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
	from oauth2client.service_account import ServiceAccountCredentials

	# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

	# 認証情報設定
	# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
	credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE_NAME, scope)

	# OAuth2の資格情報を使用してGoogle APIにログインします。
	gc = gspread.authorize(credentials)

	# 共有設定したスプレッドシート
	workbook = gc.open_by_key(SPREADSHEET_KEY)

	# ワークシート名を直接指定
	worksheet = workbook.worksheet(SPREADSHEET_NAME)

	print(worksheet.cell(1,1).value)

SPREADSHEET_KEY='1fkvKtg0UwmVbxivZQO7kjVajTAoh6WnmZaVsuSw18tU'
JSON_KEYFILE_NAME='festive-flight-306309-85a8ddf2859a.json'
SPREADSHEET_NAME='あああ'
note_title_get_from_gspread(JSON_KEYFILE_NAME,SPREADSHEET_KEY,SPREADSHEET_NAME)