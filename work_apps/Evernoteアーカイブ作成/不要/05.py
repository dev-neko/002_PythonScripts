# Google Docs API
# アーカイブに含めたい過去分のタイトルの取得までOK


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

	# プログラム実行時の1日前の日付のセルを取得
	dt_now = datetime.datetime.now()
	today_str=str(dt_now.month)+"/"+str(dt_now.day)
	today_cell = worksheet.find(today_str)

	# アーカイブに含めたい過去分のタイトルを取得
	# 全角スペースはそのままで、改行は2つのタイトルを意味しているのでリストの要素を分ける
	# 空の要素があると比較の時間が無駄なので削除
	E_col_list=[a for a in ('\n'.join(worksheet.col_values( 5)[today_cell.row:])).splitlines() if a!='']
	K_col_list=[a for a in ('\n'.join(worksheet.col_values(11)[today_cell.row:])).splitlines() if a!='']
	N_col_list=[a for a in ('\n'.join(worksheet.col_values(14)[today_cell.row:])).splitlines() if a!='']
	Q_col_list=[a for a in ('\n'.join(worksheet.col_values(17)[today_cell.row:])).splitlines() if a!='']
	T_col_list=[a for a in ('\n'.join(worksheet.col_values(20)[today_cell.row:])).splitlines() if a!='']
	W_col_list=[a for a in ('\n'.join(worksheet.col_values(23)[today_cell.row:])).splitlines() if a!='']
	X_col_list=[a for a in ('\n'.join(worksheet.col_values(24)[today_cell.row:])).splitlines() if a!='']

	# note_title_all の順番と合うように2次元配列を作成
	col_values=[]
	col_values.append(K_col_list)
	col_values.append(E_col_list)
	col_values.append(Q_col_list)
	col_values.append(N_col_list)
	col_values.append(T_col_list)
	col_values.append(X_col_list)
	col_values.append(W_col_list)

	# 辞書のキーに使用するため一旦すべてを1つのリストに結合
	title_in=['【済】Coaching Free Salon(CFS)','【済】ha-monヒーリングサロン','【済】Healing Online Salon(HOS)','【済】週刊CFS','【済】週刊HOS','【済ヒーリング】連続遠隔ヒーリング']
	title_not_in=['【済】特別儀式／鑑定']
	note_title_all=title_in+title_not_in
	# print(note_title_all)

	note_title_dict=dict(zip(note_title_all,col_values))
	# print(note_title_dict.get('【済】Coaching Free Salon(CFS)'))

	return note_title_dict

JSON_KEYFILE_NAME='spreadsheet-test-305806-b65693601679.json'
SPREADSHEET_KEY='1fkvKtg0UwmVbxivZQO7kjVajTAoh6WnmZaVsuSw18tU'
SPREADSHEET_NAME='あああ'

note_title_dict=note_title_get_from_gspread(JSON_KEYFILE_NAME,SPREADSHEET_KEY,SPREADSHEET_NAME)
# print(note_title_dict.get('【済】Coaching Free Salon(CFS)'))

print(note_title_dict['【済】Coaching Free Salon(CFS)'])
