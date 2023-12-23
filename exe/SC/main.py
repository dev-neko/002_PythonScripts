import subprocess
import time
import PySimpleGUI as sg

# ウィンドウのテーマ
sg.theme('SystemDefaultForReal')

# チェックボックスに表示する内容
check_list=[
	# 通常
	'一時的なメモ',
	'プログラミング系メモ',
	'プログラム系',
	'常用フォルダ',
	'プログラミング系フォルダ',
	'Excel系',
	'執筆フォルダ',
	'その他のメモ系',
	'test',
	'セーフモード',
]

# layout
layout=[
	[[sg.Checkbox(item,key=item)] for item in check_list],
	[sg.Button('実行',key='run'),sg.Button('終了',key='exit')],
]

# window = sg.Window('TEST', layout,size=(300, 100))
window=sg.Window('一括展開',layout,resizable=True)

while True:
	event,values=window.read()
	# 終了
	if (event==sg.WIN_CLOSED) or (event=='exit'):
		break
	# 通常
	if event=='run' and values['一時的なメモ']:
		pass
	if event=='run' and values['プログラミング系メモ']:
		open_dir=r"C:\Users\YUTAKA\PycharmProjects\memo\よく使うコマンド.txt"
		subprocess.run(['start',open_dir],shell=True)
		open_dir=r"C:\Users\YUTAKA\PycharmProjects\memo\解決したこと.txt"
		subprocess.run(['start',open_dir],shell=True)
		# pass
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
	# テスト
	if event=='run' and values['test']:
		# # Downloads
		# open_dir=r'C:\Users\YUTANAO\Downloads'
		# subprocess.run(['start','/MAX',open_dir],shell=True)
		# open_dir=r"C:\Users\YUTANAO\PycharmProjects\PythonScripts"
		# subprocess.run(['start','/MAX',open_dir],shell=True)
		# # MCalc
		# open_dir=r'C:\Users\YUTANAO\Documents\プログラム\MCalc\MCalc.exe'
		# subprocess.Popen([open_dir])
		# GoogleDriveFS
		open_dir=r"C:\Program Files\Google\Drive File Stream\55.0.3.0\GoogleDriveFS.exe"
		subprocess.Popen([open_dir])
		# Gドライブの起動待ち
		time.sleep(5)
		# 一時的なメモ
		open_dir=r'G:\マイドライブ\メモ系\一時的なメモ.txt'
		subprocess.run(['start',open_dir],shell=True)
		# なるはやでやる.smmx
		open_dir=r'G:\マイドライブ\SimpleMind\smmx\なるはやでやる.smmx'
		subprocess.run(['start','/MAX',open_dir],shell=True)
	# SM
	if event=='run' and values['セーフモード']:
		# GoogleDriveFS
		open_dir=r"C:\Program Files\Google\Drive File Stream\55.0.3.0\GoogleDriveFS.exe"
		subprocess.Popen([open_dir])
		# SRWare Iron
		open_dir=r'C:\Program Files\SRWare Iron\chrome.exe'
		subprocess.Popen([open_dir])
		# MCalc
		open_dir=r'C:\Users\YUTANAO\Documents\プログラム\MCalc\MCalc.exe'
		subprocess.Popen([open_dir])
		# 7+ Taskbar Tweaker
		open_dir=r'C:\Users\YUTANAO\AppData\Roaming\7+ Taskbar Tweaker\7+ Taskbar Tweaker.exe'
		subprocess.Popen([open_dir])
		# MouseGestureL
		open_dir=r'C:\Users\YUTANAO\Documents\プログラム\MouseGestureL\MouseGestureL.exe'
		subprocess.Popen([open_dir])
		# Screenpresso
		open_dir=r'C:\Users\YUTANAO\AppData\Local\Learnpulse\Screenpresso\Screenpresso.exe'
		subprocess.Popen([open_dir])
		# Downloads
		open_dir=r'C:\Users\YUTANAO\Downloads'
		subprocess.run(['start','/MAX',open_dir],shell=True)
		# Gドライブの起動待ち
		# 10秒では足りなかった
		time.sleep(15)
		# 一時的なメモ
		open_dir=r'H:\マイドライブ\メモ系\一時的なメモ.txt'
		subprocess.run(['start',open_dir],shell=True)
		# なるはやでやる.smmx
		open_dir=r'H:\マイドライブ\SimpleMind\smmx\なるはやでやる.smmx'
		subprocess.run(['start','/MAX',open_dir],shell=True)
		# セーフモードで使用するプログラムのSC
		# open_dir=r"C:\Users\YUTANAO\Desktop\セーフモードで使用するプログラムのSC"
		# subprocess.run(['start','/MAX',open_dir],shell=True)
	break

window.close()