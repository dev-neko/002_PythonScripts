# Evernote API
# ノートの取り扱いは画像も含めて大体OK

import re
from datetime import datetime, timezone, timedelta

# Evernote SDK for Python 3 を使う
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types



# ノートブックのタイトルごとに処理を分ける
title_in=["儀式","HOS info 抜粋","HOS info 全文"]
title_not_in=["Coaching Free Salon","ha-monヒーリングサロン","Healing Online Salon"]
# 変更後
# title_in=["【済】Coaching Free Salon(CFS)","【済】ha-monヒーリングサロン","【済】Healing Online Salon(HOS)","【済】週刊CFS","【済】週刊HOS","【済ヒーリング】連続遠隔ヒーリング"]
# title_not_in=["【済】特別儀式／鑑定"]

# アーカイブ以外のノートでアーカイブに含めるノートのタイトル
in_note_title=["あああ","えええ"]

# ノートのメディアファイル情報
resource_list=[]

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
				archive_content=reg_com_ennote.search(note_archive.content)
				archive_content=archive_content.group(1)
				print("------------------------------")
				print(f'アーカイブのタイトル：{note_archive.title}')
				print(f'アーカイブの内容：{archive_content}')
				# メディアファイル情報を取り出して配列に格納
				if note_archive.resources is not None: resource_list.extend(note_archive.resources)
				# アーカイブは1つしかないのでbreak
				break

		# 取得するノートの条件を指定 アーカイブ以外
		filter=NoteFilter()
		filter.notebookGuid=notebook.guid
		filter.words=''
		maxNotes=10
		notes_metadata_list=store.findNotesMetadata(filter,0,maxNotes,spec)
		# アーカイブ以外のノートで取り込みたいノートの内容を取得
		add_content=""
		for note_meta_data in notes_metadata_list.notes:
			note_other=store.getNote(note_meta_data.guid,True,True,True,True)
			if note_other.title in in_note_title:
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
		note_archive.content+=archive_content
		note_archive.content+=content_end
		note_archive.resources=resource_list
		store.updateNote(note_archive)