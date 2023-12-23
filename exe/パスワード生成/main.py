import PySimpleGUI as sg
import secure_pass_gen

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

# 記号の有無
kigo_frame = [
	[sg.Text("記号を")],
	[sg.Radio(text='含む', key='ON', group_id='1', default=True)],
	[sg.Radio(text='含まない', key='OFF', group_id='1', default=False)],
# 文字数
	[sg.Text("文字数")],
	[sg.Spin([i for i in range(1,100)], initial_value=12, key='LENGTH')],
# 制御ボタン
	[sg.Button('実行',key='run'),sg.Button('終了',key='exit')]
]

# 生成したパスワードをリストで出力するためのエリア
pass_frame = [
	[sg.Text("生成したパスワード")],
	[sg.Listbox([], size=(30, 10), key='PASS_LIST', enable_events=True)],
]

# コピーしたパスワードを表示するエリア
clip_frame = sg.Frame('コピーしたパスワード',layout=[
	[sg.Text('', key='CLIP_PASS', enable_events=True)],
])


layout=[
	[
		sg.Column(kigo_frame, vertical_alignment='top'),
		sg.Column(pass_frame, vertical_alignment='top')
	],
	[
		clip_frame
	]
]

window=sg.Window('パスワード生成ツール',layout,resizable=True)

while True:
	# event≒key
	event,values=window.read()
	if (event==sg.WIN_CLOSED) or (event=='exit'):
		break
	elif event=='run':
		# print(event, values)
		#
		if values['ON']:
			symbol_sw='ON'
		else:
			symbol_sw='OFF'
		cre_pass_list=[secure_pass_gen.pass_gen(values['LENGTH'],symbol_sw) for i in range(10)]
		# windowのkeyがPASS_LISTの内容をcre_pass_listに変更する
		window['PASS_LIST'].update(cre_pass_list)
	# リストのパスワードがクリックされた時の処理
	elif event=='PASS_LIST':
		# クリップボードをクリア
		window['PASS_LIST'].Widget.clipboard_clear()
		# クリップボードにコピー
		window['PASS_LIST'].Widget.clipboard_append(values['PASS_LIST'][0])
		# コピーしたパスワードを表示
		window['CLIP_PASS'].update(values['PASS_LIST'][0])

window.close()