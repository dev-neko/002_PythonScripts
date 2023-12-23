# Evernote API と Google Docs API を結合
# アーカイブの内容はすべて再取得するので、元のアーカイブの内容は取得しなくてOK



import re
from datetime import datetime, timezone, timedelta

# Evernote SDK for Python 3 を使う
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

def note_title_get_from_gspread(JSON_KEYFILE_NAME,SPREADSHEET_KEY,SPREADSHEET_NAME,title_in,title_not_in):

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
	note_title_all=title_in+title_not_in
	# print(note_title_all)

	note_title_dict=dict(zip(note_title_all,col_values))
	# print(note_title_dict.get('【済】Coaching Free Salon(CFS)'))

	return note_title_dict



# ノートブックのタイトルごとに処理を分ける
# title_in=["儀式","HOS info 抜粋","HOS info 全文"]
# title_not_in=["Coaching Free Salon","ha-monヒーリングサロン","Healing Online Salon"]
# 変更後
title_in=["【済】Coaching Free Salon(CFS)","【済】ha-monヒーリングサロン","【済】Healing Online Salon(HOS)","【済】週刊CFS","【済】週刊HOS","【済ヒーリング】連続遠隔ヒーリング"]
title_not_in=["【済】特別儀式／鑑定"]

# アーカイブ以外のノートでアーカイブに含めるノートのタイトル
# in_note_title=["あああ","えええ"]
JSON_KEYFILE_NAME='spreadsheet-test-305806-b65693601679.json'
SPREADSHEET_KEY='1fkvKtg0UwmVbxivZQO7kjVajTAoh6WnmZaVsuSw18tU'
SPREADSHEET_NAME='あああ'
note_title_dict=note_title_get_from_gspread(JSON_KEYFILE_NAME,SPREADSHEET_KEY,SPREADSHEET_NAME,title_in,title_not_in)

# ノートの事前情報
note_header='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
content_start='<en-note>'
content_end='</en-note>'
reg_com_ennote=re.compile("%s(.*?)%s"%(content_start,content_end))

# evernote.api.client.EvernoteClient を初期化
client = EvernoteClient(
	token   = 'S=s486:U=d5b629e:E=17f152d5196:C=177bd7c2208:P=185:A=tx0r8098p1:V=2:H=f8a6604c96ac54a5def6b0e3992e899d', # アクセストークンを指定
	sandbox = False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

# evernote.api.client.Store を取得
store = client.get_note_store()

# ノートブックのリストを取得
notebook_list = store.listNotebooks()

# NoteMetadata に含めるフィールドを設定
spec=NotesMetadataResultSpec()
spec.includeTitle=True
spec.includeCreated=True
spec.includeAttributes=True



for notebook in notebook_list:

	if notebook.name in title_in or notebook.name in title_not_in:

		print("------------------------------")
		print("------------------------------")
		print(f'ノートブック名：{notebook.name}')

		# 取得するノートの条件を指定 アーカイブのみ
		filter=NoteFilter()
		filter.notebookGuid=notebook.guid
		filter.words='【アーカイブ】'
		maxNotes=10
		notes_metadata_list=store.findNotesMetadata(filter,0,maxNotes,spec)
		# アーカイブの内容を取得
		for note_meta_data in notes_metadata_list.notes:
			note_archive=store.getNote(note_meta_data.guid,True,True,True,True)
			if "【アーカイブ】" in note_archive.title:
				# アーカイブは1つしかないのでbreak
				break

		# 取得するノートの条件を指定 アーカイブ以外
		filter=NoteFilter()
		filter.notebookGuid=notebook.guid
		filter.words=''
		maxNotes=10
		notes_metadata_list=store.findNotesMetadata(filter,0,maxNotes,spec)
		# アーカイブ以外のノートで取り込みたいノートの内容を取得
		# 追加するコンテンツ文字列
		add_content=""
		# ノートのメディアファイル情報
		resource_list=[]
		for hope_note_title in note_title_dict[notebook.name]:
			for note_meta_data in notes_metadata_list.notes:
				note_other=store.getNote(note_meta_data.guid,True,True,True,True)
				if note_other.title==hope_note_title:
					other_content=reg_com_ennote.search(note_other.content)
					other_content=other_content.group(1)
					# アーカイブにノートのタイトルを含めるか分岐
					if notebook.name in title_in:
						other_content_title="<div>"+note_other.title+'</div>'
					else:
						other_content_title=""
					add_content+=other_content_title+other_content+"<div><hr></hr></div>"
					# メディアファイル情報を取り出して配列に格納
					if note_other.resources is not None: resource_list.extend(note_other.resources)
					print("------------------------------")
					print(f'追加するノートのタイトル：{note_other.title}')
					print(f'追加するノートの内容：{other_content}')

		# アーカイブを編集して保存
		note_archive.content=note_header
		note_archive.content+=content_start
		note_archive.content+=add_content
		note_archive.content+=content_end
		note_archive.resources=resource_list
		store.updateNote(note_archive)