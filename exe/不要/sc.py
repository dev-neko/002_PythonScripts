import subprocess
import tkinter
from tkinter import *
from tkinter import font

# Tkクラスを生成して展開したい要素を返す
def cre_tkinter(chk_txt):

	# ボタンクリックイベント(チェック初期値をセット)
	def btn_click(bln):
		for i in range(len(chk_bln)):
			chk_bln[i].set(bln)

	# Tkクラス生成
	root = Tk()
	# 画面サイズ
	root.geometry()
	root.resizable(False, False)
	# 画面タイトル
	root.title('一括展開')

	# Frameを設定
	frame_label=Frame(root)
	frame_chk=Frame(root)
	frame_btn=Frame(root)
	# widgetの配置を設定
	padx=10
	pady=5
	frame_label.grid(row=0, column=0, padx=padx, pady=pady)
	frame_chk.grid(row=1, column=0, padx=padx, pady=pady)
	frame_btn.grid(row=2, column=0, padx=padx, pady=pady,sticky=(N,S,E,W))

	# フォントオブジェクトを新規に作成
	my_font=font.Font(root,family='BIZ UDゴシック',size=16)
	my_font_12=font.Font(root,family='BIZ UDゴシック',size=12)

	label = Label(frame_label, text='一括展開する項目の選択', font=my_font_12)
	label.grid()

	# チェックボックスON/OFF状態のリスト
	chk_bln={}
	# 未選択状態のチェックボタンを動的に作成して配置
	for i in range(len(chk_txt)):
		chk_bln[i] = BooleanVar(value=False)
		chk = Checkbutton(frame_chk, variable=chk_bln[i], text=chk_txt[i], font=my_font)
		chk.grid(sticky=W)

	# ボタン作成
	btn = Button(frame_btn, text="実行", command=root.destroy, font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text="終了", command=sys.exit, font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)
	btn = Button(frame_btn, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
	btn.pack(expand=True,fill=tkinter.X,pady=1)

	# イベントループ開始
	root.mainloop()

	# チェックを入れたテキストを配列に入れる
	result_list=[]
	for i in range(len(chk_bln)):
		if chk_bln[i].get(): result_list.append(chk_txt[i])

	return result_list

# チェック判定して展開
def open_process(result_list):
	try:
		if '秀丸メモ系' in result_list:
			open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\すぐやる事.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\メモ.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\時間あるときにやる事.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\ブログネタ.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\こうしておけばよかった.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			# open_dir = r'C:\Users\YUTANAO\Dropbox\メモ系\荒野行動攻略まとめ.txt'
			# subprocess.run(['start', '/MAX', open_dir], shell=True)
			open_dir=r'C:\Users\YUTANAO\Documents\Python\Linuxのメモ.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Documents\Python\Pythonのメモ.txt'
			subprocess.run(['start','/MAX',open_dir],shell=True)
		if '一時的なメモ' in result_list:
			#open_dir=r'C:\Users\YUTANAO\Dropbox\メモ系\一時的なメモ.txt'
			# PCがSMでしか起動しなくなったので一時的に変更
			open_dir=r'G:\マイドライブ\メモ系\一時的なメモ.txt'
			subprocess.run(['start',open_dir],shell=True)
		if 'プログラミング系のメモ' in result_list:
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\memo\cloneしたらやる事.txt"
			subprocess.run(['start',open_dir],shell=True)
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\memo\メモ.txt"
			subprocess.run(['start',open_dir],shell=True)
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\memo\よく使うコマンド.txt"
			subprocess.run(['start',open_dir],shell=True)
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\memo\解決したこと.txt"
			subprocess.run(['start',open_dir],shell=True)
		if 'Excel系' in result_list:
			open_dir=r'C:\Users\YUTANAO\Dropbox\予定・結果表_2021.xlsx'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			# open_dir = r'C:\Users\YUTANAO\Dropbox\MNPまとめ.xlsx'
			# subprocess.run(['start', '/MAX', open_dir], shell=True)
			# open_dir=r'C:\Users\YUTANAO\Dropbox\IPOまとめ.xlsx'
			# subprocess.run(['start','/MAX',open_dir],shell=True)
		if 'プログラム系' in result_list:
			open_dir=r'C:\Program Files\SRWare Iron\chrome.exe'
			subprocess.Popen([open_dir],shell=True)
			open_dir=r'C:\Program Files\ModelMakerTools\SimpleMind\1.23.0\SimpleMindPro.exe'
			subprocess.Popen([open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Documents\プログラム\MCalc\MCalc.exe'
			subprocess.Popen([open_dir],shell=True)
			# 開けなかったので一旦保留
			# open_dir=r'"C:\Program Files\Google\Chrome\Application\chrome_proxy.exe"  "--profile-directory=Profile 1" "--app-id=lainlkmlgipednloilifbppmhdocjbda"'
			# subprocess.Popen([open_dir],shell=True)
		# 常用フォルダ
		if '常用フォルダ' in result_list:
			open_dir=r'C:\Users\YUTANAO\Downloads'
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\PythonScripts"
			subprocess.run(['start','/MAX',open_dir],shell=True)
			open_dir=r"C:\Users\YUTANAO\PycharmProjects\PythonApps"
			subprocess.run(['start','/MAX',open_dir],shell=True)
		# 執筆フォルダ
		if '執筆フォルダ' in result_list:
			open_dir=r'C:\Users\YUTANAO\Documents\Python\keys'
			subprocess.run(['explorer',open_dir],shell=True)
			open_dir=r'C:\Users\YUTANAO\Documents\執筆'
			subprocess.run(['explorer',open_dir],shell=True)
			# open_dir = r'C:\Users\YUTANAO\Documents\執筆\下書きOK'
			# subprocess.run(['explorer', open_dir], shell=True)
	except Exception as err:
		print(f'エラー内容\n{err}')
	finally:
		input('エンターを入力してプログラムを終了。')
		sys.exit()

chk_txt = ['一時的なメモ','プログラミング系のメモ','プログラム系','常用フォルダ','Excel系','執筆フォルダ','秀丸メモ系',]
open_process(cre_tkinter(chk_txt))