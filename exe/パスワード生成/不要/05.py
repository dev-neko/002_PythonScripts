import os
import random
import PySimpleGUI as sg

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

# チェックボックスに表示する内容
check_list=[
	'一時的なメモ',
	'プログラミング系メモ',
	'プログラム系',
	'常用フォルダ',
	'プログラミング系フォルダ',
	'Excel系',
	'執筆フォルダ',
	'その他のメモ系',
]
check_list_2=[
	'aaa',
	'ccc',
	'bbb',
]

#sg.Frameでフレームを定義
#フレーム1
frame1 = sg.Frame('通常',[
	[[sg.Checkbox(item,key=item)] for item in check_list],
])
#フレーム2
frame2 = sg.Frame('SM',[
	[sg.Checkbox(item,key=item) for item in check_list_2],
])

# layout
layout=[
	[sg.Text('チェックボックス')],
	[frame1],
	[frame2],
	[sg.Button('実行',key='run'),sg.Button('終了',key='exit')],
]

# window = sg.Window('TEST', layout,size=(300, 100))
window = sg.Window('TEST',layout,resizable=True)

while True:
	event, values = window.read()
	if (event == sg.WIN_CLOSED) or (event == 'exit'):
			break

	# print(values)  # {'check_A': True, 'check_B': False}  ←-- A を押したときの POST 値

	if event == 'run' and values['一時的なメモ']:
		pass
	if event == 'run' and values['プログラミング系のメモ']:
		pass
	if event=='run' and values['プログラム系']:
		pass
	if event=='run' and values['常用フォルダ']:
		pass
	if event=='run' and values['プログラミング系フォルダ']:
		pass
	if event=='run' and values['Excel系']:
		pass
	if event=='run' and values['執筆フォルダ']:
		pass
	if event=='run' and values['その他のメモ系']:
		pass






window.close()