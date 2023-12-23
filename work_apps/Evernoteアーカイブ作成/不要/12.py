"""
本番EvernoteTokenを使用してテスト

アーカイブを取得するだけ

帯域制限対応版
"""



import re
import sys
import tkinter.font
from tkinter import *

# Evernote SDK for Python 3 を使う
from tkinter import messagebox

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types



def get_notes_metadata_list(notebook,words):
	# NoteMetadata に含めるフィールドを設定 タイトルのみ
	spec=NotesMetadataResultSpec()
	spec.includeTitle=True
	# タイトルでフィルタ
	filter=NoteFilter()
	filter.notebookGuid=notebook.guid
	filter.words='intitle:'+words
	offset=0
	maxNotes=2
	notes_metadata_list=store.findNotesMetadata(filter,offset,maxNotes,spec)
	return notes_metadata_list.notes
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
	"""
	【済】ha-monヒーリングサロン⇒E列
	【済】Coaching Free Salon(CFS)⇒K列
	【済】週刊CFS⇒N列
	【済】Healing Online Salon(HOS)⇒Q列
	【済】週刊HOS⇒T列
	【済】特別儀式／鑑定⇒W列
	【済ヒーリング】連続遠隔ヒーリング⇒X列
	
	【済】ha-monヒーリングサロン
	【済】Coaching Free Salon(CFS)
	【済】週刊CFS
	【済】Healing Online Salon(HOS)
	【済】週刊HOS
	【済】特別儀式／鑑定
	【済ヒーリング】連続遠隔ヒーリング
	"""
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
def cre_tkinter(title_in,title_not_in):
	# ボタンクリックイベント(チェック初期値をセット)
	def btn_click(bln):
		for i in range(len(chk_bln)):
			chk_bln[i].set(bln)

	# Tkクラス生成
	root = Tk()
	# 画面サイズ
	root.geometry()
	root.resizable(False, False)
	# 画面タイトル
	root.title('Evernote整理アプリ')

	# Frameを設定
	frame_label=Frame(root)
	frame_chk=Frame(root)
	frame_btn=Frame(root)
	# widgetの配置を設定
	padx=10
	pady=5
	frame_label.grid(row=0, column=0, padx=padx, pady=pady)
	frame_chk.grid(row=1, column=0, padx=padx, pady=pady)
	frame_btn.grid(row=2, column=0, padx=padx, pady=pady,sticky=(N,S,E,W))

	# フォントオブジェクトを新規に作成
	my_font = font.Font(root,family='BIZ UDゴシック',size=12)

	label = Label(frame_label, text='アーカイブを作成するノートブック名を選択してください。')
	label.grid()

	# チェックボタンのラベルをリスト化する
	chk_txt=title_in+title_not_in
	# チェックボックスON/OFFの状態
	chk_bln = {}
	# チェックボタンを動的に作成して配置
	for i in range(len(chk_txt)):
		chk_bln[i] = BooleanVar(value=True)
		chk = Checkbutton(frame_chk, variable=chk_bln[i], text=chk_txt[i], font=my_font)
		chk.grid(sticky=W)

	# ボタン作成
	btn = Button(frame_btn, text="実行", command=root.destroy, font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text="終了", command=sys.exit, font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
	btn.pack(expand=True,fill=tkinter.X)

	# イベントループ開始
	root.mainloop()

	# チェックを入れたテキストを配列に入れる
	return_list=[]
	for i in range(len(chk_bln)):
		if chk_bln[i].get(): return_list.append(chk_txt[i])

	return return_list



# ノートブックのタイトルごとに処理を分ける
title_in=["【済】Coaching Free Salon(CFS)","【済】ha-monヒーリングサロン","【済】Healing Online Salon(HOS)","【済】週刊CFS","【済】週刊HOS","【済ヒーリング】連続遠隔ヒーリング"]
title_not_in=["【済】特別儀式／鑑定"]

# ノートの事前情報
note_header='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
content_start='<en-note>'
content_end='</en-note>'
reg_com_ennote=re.compile("%s(.*?)%s"%(content_start,content_end))

# evernote.api.client.EvernoteClient を初期化
client=EvernoteClient(
	token='S=s689:U=c22bf0a:E=17f4ac5f9a1:C=177f314ca50:P=185:A=kanricenter123:V=2:H=06e31b7feb049ea0edafa8706fd303ed', # アクセストークンを指定
	sandbox=False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

# evernote.api.client.Store を取得
store = client.get_note_store()

# ノートブックのリストを取得
notebook_list = store.listNotebooks()

# tkinterでチェックを入れたノートブックのタイトルを取得
tk_chk_list=cre_tkinter(title_in,title_not_in)
print(tk_chk_list)


for notebook in notebook_list:

	if notebook.name in tk_chk_list:

		print("------------------------------")
		print("------------------------------")
		print(f'ノートブック名：{notebook.name}')

		# アーカイブの内容を取得
		notes_metadata_list=get_notes_metadata_list(notebook,'【アーカイブ】')
		note_count=len(notes_metadata_list)
		# 部分一致で検索するけど1つのノートだけに【アーカイブ】と入れているはずなのでそれ以外はエラー
		if note_count>1:
			# print("------------------------------")
			# for notes_metadata in notes_metadata_list:
			# 	note_archive=store.getNote(notes_metadata.guid,True,True,True,True)
			# 	print(f'検出したアーカイブのタイトル：{note_archive.title}')
			# print(f'アーカイブの内容：{note_archive.content}')
			print("------------------------------")
			print("アーカイブが複数あります。")
		elif note_count==0:
			print("------------------------------")
			print("アーカイブが見つかりません。")
		elif note_count==1:
			note_archive=store.getNote(notes_metadata_list[0].guid,True,True,True,True)
			print("------------------------------")
			print(f'正常に検出されたアーカイブのタイトル：{note_archive.title}')

		# messagebox.showinfo("")