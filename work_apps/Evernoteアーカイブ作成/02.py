"""
質問用に編集
"""

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
# レートリミットの例外
from evernote.edam.error.ttypes import EDAMSystemException

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

		if notebook.name in '【済】Coaching Free Salon(CFS)':

			print("------------------------------")
			print("------------------------------")
			print(f'ノートブック名：{notebook.name}')

			# アーカイブの内容を取得
			spec=NotesMetadataResultSpec()
			spec.includeTitle=True
			filter=NoteFilter()
			filter.notebookGuid=notebook.guid
			filter.words='無'
			offset=0
			maxNotes=2
			notes_metadata_list=store.findNotesMetadata(filter,offset,maxNotes,spec)
			print(notes_metadata_list)

			for notes_metadata in notes_metadata_list.notes:
				note_archive=store.getNote(notes_metadata.guid,True,True,True,True)
				print("------------------------------")
				print(f'検出されたノートのタイトル：{note_archive.title}')
except EDAMSystemException as err:
	print("------------------------------")
	print(f'EvernoteAPIのレート制限に達しました。\n{err.rateLimitDuration} 秒後に再試行して下さい。')