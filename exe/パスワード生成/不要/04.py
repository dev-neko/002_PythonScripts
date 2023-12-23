import os
import random
import PySimpleGUI as sg

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

layout = [
	[sg.Text('チェックボックス')],
	[sg.Checkbox('秀丸メモ系', key='秀丸メモ系')],
	[sg.Checkbox('一時的なメモ', key='一時的なメモ')],
	[sg.Checkbox('プログラミング系のメモ', key='プログラミング系のメモ')],
	[sg.Checkbox('A', key='check_A')],
	[sg.Checkbox('A', key='check_A')],
	[sg.Checkbox('A', key='check_A')],
	[sg.Checkbox('A', key='check_A')],
	[sg.Button('実行',key='run')],
	[sg.Button('終了',key='exit')],
	[sg.Button('全てにチェックを入れる',key='run')],
	[sg.Button('全てのチェックを外す',key='run')],
]

# window = sg.Window('TEST', layout,size=(300, 100))
window = sg.Window('TEST',layout)

while True:
		event, values = window.read()
		if (event == sg.WIN_CLOSED) or (event == 'exit'):
				break

		print(values)  # {'check_A': True, 'check_B': False}  ←-- A を押したときの POST 値

		# if event == 'button':
		#     print('normal')

		if event == 'button' and values['check_A']:
				print('モードA')

		if event == 'button' and values['check_B']:
				print('モードB')

#仮として、'モードA'や'モードB'が表示できるようになりたい。

window.close()