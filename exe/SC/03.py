import PySimpleGUI as sg

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

# ウィンドウのレイアウト
layout = [
	[sg.Text('チェックボックス')],
	[sg.Checkbox("チェックボックス1", default=True)],
	[sg.Checkbox("チェックボックス2", default=False)]
]

# ウィンドウオブジェクトの作成
window = sg.Window('title', layout)

# イベントのループ
while True:
	# イベントの読み込み
	event, values = window.read()
	# ウィンドウの×ボタンクリックで終了
	if event == sg.WIN_CLOSED:
		break

# ウィンドウ終了処理
window.close()