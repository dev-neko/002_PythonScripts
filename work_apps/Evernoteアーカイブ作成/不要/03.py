# API使用 添付データの取り扱いで苦戦して中断

import re
from datetime import datetime, timezone, timedelta

# Evernote SDK for Python 3 を使う
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec



title_in=["儀式","HOS info 抜粋","HOS info 全文"]
title_not_in=["Coaching Free Salon","ha-monヒーリングサロン","Healing Online Salon"]

note_header='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
content_start='<en-note>'
content_end='</en-note>'
reg_com_ennote=re.compile("%s(.*?)%s"%(content_start,content_end))
reg_com_objID=re.compile("%s(.*?)%s"%('objID="','"'))

# evernote.api.client.EvernoteClient を初期化
client = EvernoteClient(
	token   = 'S=s486:U=d5b629e:E=17f152d5196:C=177bd7c2208:P=185:A=tx0r8098p1:V=2:H=f8a6604c96ac54a5def6b0e3992e899d', # アクセストークンを指定
	sandbox = False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

# evernote.api.client.Store を取得
store = client.get_note_store()

# ノートブックのリストを取得
notebook_list = store.listNotebooks()

for notebook in notebook_list:

	if notebook.name in title_in:

		print("------------------------------")
		print("------------------------------")
		print(f'ノートブック名：{notebook.name}')

		# NoteMetadata に含めるフィールドを設定
		spec = NotesMetadataResultSpec()
		spec.includeTitle=True
		spec.includeCreated=True
		spec.includeAttributes=True

		# 取得するノートの条件を指定 アーカイブのみ
		filter_archive = NoteFilter()
		filter_archive.notebookGuid = notebook.guid
		filter_archive.words='【アーカイブ】'
		notes_metadata_list_archive = store.findNotesMetadata(filter_archive,0,10,spec)

		# アーカイブの内容を取得
		for note_meta_data in notes_metadata_list_archive.notes:
			note_archive=store.getNote(note_meta_data.guid,True,True,True,True)
			if "【アーカイブ】" in note_archive.title:
				archive_content=reg_com_ennote.search(note_archive.content)
				archive_content=archive_content.group(1)
				break
		print(f'アーカイブの内容：{archive_content}')

		# 取得するノートの条件を指定 アーカイブ以外
		filter_other = NoteFilter()
		filter_other.notebookGuid = notebook.guid
		maxNotes=10
		notes_metadata_list_other = store.findNotesMetadata(filter_other,0,maxNotes,spec)

		# アーカイブ以外のノートで取り込みたいノートの内容を取得
		add_content=""
		for note_meta_data in notes_metadata_list_other.notes:
			note_other=store.getNote(note_meta_data.guid,True,True,True,True)
			if "えええ"==note_other.title:
				other_content=reg_com_ennote.search(note_other.content)
				other_content=other_content.group(1)
				other_content_title="<div>"+note_other.title+'</div><div><br clear="none"/></div>'
				add_content+=other_content_title+other_content+"<div><hr></hr></div>"
				print(f'追加するノートのタイトル：{note_other.title}')
				print(f'追加するノートの内容：{other_content}')

				# メモに埋め込まれていたり添付されているメディアファイル情報を取り出す
				if note_other.resources is not None:
					# evernote.edam.type.ttypes.Resource を取り出す

					for resource in note_other.resources:
						aaa=reg_com_objID.search(str(resource.recognition.body))
						aaa=aaa.group(1)
						# print(f'添付データhash:{aaa}')
						# print(f'添付データguid:{resource.guid}')
						# print(f'添付データファイル名:{resource.attributes.fileName}')
						# print(f'データタイプ:{resource.mime}')
						# class とか data-mce-src が含まれてるとエラーになる？
						# <en-media> があるとただの空白になるので画像タグと置換？
						# data_url='<div><img src="https://www.evernote.com/shard/s486/res/'+resource.guid+'/'+resource.attributes.fileName+'" alt="" name="'+resource.guid+'" class="en-media" data-mce-src="https://www.evernote.com/shard/s486/res/'+resource.guid+'/'+resource.attributes.fileName+'"></div>'
						data_url='<div><img src="https://www.evernote.com/shard/s486/res/'+resource.guid+'/'+resource.attributes.fileName+'"></img></div>'
						print(f'置換先:{data_url}')
						tikan='<en-media hash="'+aaa+'" type="'+resource.mime+'"></en-media>'
						print(f'置換元:{tikan}')
						# add_content=add_content.replace(tikan,data_url)
						# ただ置換しただけだと画像のサイズ情報などが含まれなくて元の画像のサイズで表示される
						# add_content+=str(resource)

		# add_content='<div><img class="en-media" src="https://www.evernote.com/shard/s486/res/9df4c626-ccb3-4547-9d22-641eea2ebcf4/+.jpg" alt="" name="9df4c626-ccb3-4547-9d22-641eea2ebcf4" data-mce-src="https://www.evernote.com/shard/s486/res/9df4c626-ccb3-4547-9d22-641eea2ebcf4/+.jpg"></div>'
		# add_content='<div><img src="https://www.evernote.com/shard/s486/res/9df4c626-ccb3-4547-9d22-641eea2ebcf4/+.jpg"></img></div>'
		# アーカイブを編集して保存
		note_archive.content=note_header
		note_archive.content+=content_start
		note_archive.content+=add_content
		print(f'追加するコンテンツ:{add_content}')
		note_archive.content+=archive_content
		note_archive.content+=content_end
		store.updateNote(note_archive)

# elif notebook.name in title_not_in:
	#
	# 	print("------------------------------")
	# 	print("------------------------------")
	# 	print(f'ノートブック名: {notebook.name}')
	#
	# 	# 取得するノートの条件を指定
	# 	filter = NoteFilter()
	# 	filter.notebookGuid = notebook.guid # ノートブックの GUID を指定
	#
	# 	# NoteMetadata に含めるフィールドを設定
	# 	spec = NotesMetadataResultSpec()
	# 	spec.includeTitle=True
	# 	spec.includeCreated=True
	# 	spec.includeAttributes=True
	#
	# 	# ノートのメタデータのリスト evernote.edam.notestore.ttypes.NotesMetadataList を取得
	# 	note_max=1
	# 	notes_metadata_list = store.findNotesMetadata(filter,0,note_max,spec)
	#
	# 	# evernote.edam.notestore.ttypes.NoteMetadata を取り出す
	# 	for note_meta_data in notes_metadata_list.notes:
	#
	# 		# evernote.edam.type.ttypes.Note を取得
	# 		note = store.getNote(note_meta_data.guid,True,True,True,True)
	# 		print("------------------------------")
	# 		print(f'内容(XHTML): {note.content}')