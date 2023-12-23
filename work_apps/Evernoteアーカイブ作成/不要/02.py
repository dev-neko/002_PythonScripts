# API使用 サンプルそのまま



from datetime import datetime, timezone, timedelta

# Evernote SDK for Python 3 を使う
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

# evernote.api.client.EvernoteClient を初期化
client = EvernoteClient(
	token   = 'S=s486:U=d5b629e:E=17f152d5196:C=177bd7c2208:P=185:A=tx0r8098p1:V=2:H=f8a6604c96ac54a5def6b0e3992e899d', # アクセストークンを指定
	sandbox = False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

# evernote.api.client.Store を取得
store = client.get_note_store()

# ノートブック evernote.edam.type.ttypes.Notebook のリストを取得
notebook_list = store.listNotebooks()
print(f'ノートブックの数: {len(notebook_list)}')

# evernote.edam.type.ttypes.Notebook を取り出す
for notebook in notebook_list:

	print(f'ノートブック名: {notebook.name}')

	# 取得するノートの条件を指定
	filter = NoteFilter()
	filter.notebookGuid = notebook.guid # ノートブックの GUID を指定

	# NoteMetadata に含めるフィールドを設定
	spec = NotesMetadataResultSpec()
	spec.includeTitle      = True
	spec.includeCreated    = True
	spec.includeAttributes = True

	# ノートのメタデータのリスト evernote.edam.notestore.ttypes.NotesMetadataList を取得
	notes_metadata_list = store.findNotesMetadata(
		filter,
		0, # offset 条件にヒットした一覧から取得したいインデックス位置を指定
		1, # maxNotes 取得するノート数の最大値。今回は最大で1つだけ取得する
		spec)

	print(f'ノートブックに含まれるノートの数: {notes_metadata_list.totalNotes}')

	# evernote.edam.notestore.ttypes.NoteMetadata を取り出す
	for note_meta_data in notes_metadata_list.notes:

		print(f'  ノートのタイトル: {note_meta_data.title}')

		# evernote.edam.type.ttypes.Note を取得
		note = store.getNote(
			note_meta_data.guid, # ノートの GUID を指定
			True, # withContent
			True, # withResourcesData
			True, # withResourcesRecognition
			True) # withResourcesAlternateData
		print(f'    タイトル: {note.title}')
		print(f'    作成日時: {datetime.fromtimestamp(note.created / 1000, timezone(timedelta(hours=9)))}')
		print(f'    内容(XHTML): {note.content}') # 長いので先頭64文字だけ取り出す

		# メモに埋め込まれていたり添付されているメディアファイル情報を取り出す
		if note.resources is not None:
			# evernote.edam.type.ttypes.Resource を取り出す
			for resource in note.resources:
				print(f'    添付データファイル名: {resource.attributes.fileName}')
				print(f'      データタイプ: {resource.mime}')