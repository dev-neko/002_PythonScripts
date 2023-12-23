import subprocess
import time
import PySimpleGUI as sg
import secure_pass_gen

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

# 記号の有無
kigo_frame = sg.Frame('記号を',layout=[
	# []で要素を囲むと縦並びになる、外すと横並び
	# [[sg.Radio(item[1], key=item[0], group_id='0')] for item in radio_dic.items()],
	# 初期値を設定するためにそれぞれ設定
	[sg.Radio(text='含む', key='ON', group_id='1', default=True)],
	[sg.Radio(text='含まない', key='OFF', group_id='1', default=False)],
])

# 文字数
moji_frame = sg.Frame('文字数',layout=[
	[sg.Spin([i for i in range(1,100)], initial_value=12, key='LENGTH')]
])

# 生成したパスワードをリストで出力するためのエリア
pass_frame = sg.Frame('生成したパスワード',layout=[
	[sg.Listbox([], size=(20, 10), key='PASS_LIST', enable_events=True)],
])

layout=[
	[[[kigo_frame,],[moji_frame,]],[pass_frame,]]
	# [sg.Button('実行',key='run'),sg.Button('終了',key='exit')],
]

# window = sg.Window('TEST', layout,size=(300, 100))
window=sg.Window('パスワード生成ツール',layout,resizable=True)

while True:
	# event≒key
	event,values=window.read()
	if (event==sg.WIN_CLOSED) or (event=='exit'):
		break
	elif event=='run':
		print(event, values)
		#
		if values['ON']:
			symbol_sw='ON'
		else:
			symbol_sw='OFF'
		cre_pass_list=[secure_pass_gen.pass_gen(values['LENGTH'],symbol_sw) for i in range(10)]
		# windowの中のkeyがrunの内容をaaaに変更する
		# window['run'].update('aaaa')

		# ラジオボタンを選んだ状態のままにする

		window['PASS_LIST'].update(cre_pass_list)
	# リストのパスワードがクリックされた時の処理
	elif event=='PASS_LIST':
		# ポップアップを表示
		# sg.popup(f"あなたの好きな色は、{values['PASS_LIST'][0]}ですね。")
		# クリップボードにコピー
		window['PASS_LIST'].Widget.clipboard_append(values['PASS_LIST'][0])

window.close()
