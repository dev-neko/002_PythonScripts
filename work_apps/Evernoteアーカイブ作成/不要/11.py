import re
import sys
import tkinter.font
from tkinter import *

# Evernote SDK for Python 3 を使う
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types



# evernote.api.client.EvernoteClient を初期化
client=EvernoteClient(
	token='S=s689:U=c22bf0a:E=17f4ac5f9a1:C=177f314ca50:P=185:A=kanricenter123:V=2:H=06e31b7feb049ea0edafa8706fd303ed', # アクセストークンを指定
	sandbox=False # Sandbox ではなく Production 環境を使う場合は明示的に False を指定
)

# evernote.api.client.Store を取得
store = client.get_note_store()

# ノートブックのリストを取得
notebook_list = store.listNotebooks()

for notebook in notebook_list:
	print(notebook.name)