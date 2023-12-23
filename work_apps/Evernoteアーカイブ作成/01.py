"""
Evernote API と Google Docs API を統合
アーカイブの内容はすべて再取得するので、元のアーカイブの内容は取得しなくてOK
フィルターでノートのタイトル検索をすることでノートブック内のノート数が250件以上でも対応可能にした
これで大体OKのはず

tkinterと統合した

本番EvernoteTokenを使用してテスト
帯域制限対応版

帯域制限に対応させても制限掛かるので、指定された秒数だけ待機する処理を追加
"""



import re
import sys
import tkinter.font
from tkinter import *
from tkinter import messagebox

# Evernote SDK for Python 3 を使う
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

# レートリミットの例外
from evernote.edam.error.ttypes import EDAMSystemException

# ？
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

# xmlの解析に使用
import xml.etree.ElementTree

def get_notes_metadata_list(notebook,words):
	# NoteMetadata に含めるフィールドを設定 タイトルのみ
	spec=NotesMetadataResultSpec()
	spec.includeTitle=True
	# タイトルでフィルタ
	filter=NoteFilter()
	filter.notebookGuid=notebook.guid
	filter.words=words
	offset=0
	maxNotes=2
	notes_metadata_list=store.findNotesMetadata(filter,offset,maxNotes,spec)
	return notes_metadata_list.notes
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
		chk_bln[i] = BooleanVar(value=False)
		chk = Checkbutton(frame_chk, variable=chk_bln[i], text=chk_txt[i], font=my_font)
		chk.grid(sticky=W)

	# ボタン作成
	btn = Button(frame_btn, text="実行", command=root.destroy, font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text="終了", command=sys.exit, font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)

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

# tkinterでチェックを入れたノートブックのタイトルを取得
# tk_chk_list=cre_tkinter(title_in,title_not_in)
# print(tk_chk_list)
tk_chk_list=['【済】Coaching Free Salon(CFS)']

# evernote.api.client.EvernoteClient を初期化
client=EvernoteClient(
	token='S=s689:U=c22bf0a:E=17f4ac5f9a1:C=177f314ca50:P=185:A=kanricenter123:V=2:H=06e31b7feb049ea0edafa8706fd303ed', # アクセストークンを指定
	sandbox=False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

try:
	# evernote.api.client.Store を取得
	store = client.get_note_store()

	# ノートブックのリストを取得
	notebook_list = store.listNotebooks()

	# アーカイブとアーカイブに追加するノートの取得
	for notebook in notebook_list:

		if notebook.name in tk_chk_list:

			print("------------------------------")
			print("------------------------------")
			print(f'ノートブック名：{notebook.name}')

			# アーカイブの内容を取得
			notes_metadata_list=get_notes_metadata_list(notebook,'アーカイブ')
			note_count=len(notes_metadata_list)
			# 部分一致で検索するけど1つのノートだけに【アーカイブ】と入れているはずなのでそれ以外はエラー
			for notes_metadata in notes_metadata_list:
				note_archive=store.getNote(notes_metadata.guid,True,True,True,True)
				print("------------------------------")
				print(f'検出されたノートのタイトル：{note_archive.title}')
except EDAMSystemException as err:
	print("------------------------------")
	print(f'EvernoteAPIのレート制限に達しました。\n{err.rateLimitDuration} 秒後に再試行して下さい。')