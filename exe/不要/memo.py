import subprocess
import tkinter.font
import sys


# Tkクラス生成
tki = tkinter.Tk()
# 画面サイズ
tki.geometry('300x400')
# 画面タイトル
tki.title('一括展開')

# フォントオブジェクトを新規に作成
my_font = tkinter.font.Font(tki,family='BIZ UDゴシック',size=16)

# チェックボタンのラベルをリスト化する
chk_txt = ['秀丸メモ系','Excel系','一時的なメモ','フォルダ系','プログラム系']
# チェックボックスON/OFFの状態
chk_bln = {}
# チェックボタンを動的に作成して配置
for i in range(len(chk_txt)):
	chk_bln[i] = tkinter.BooleanVar()
	chk = tkinter.Checkbutton(tki, variable=chk_bln[i], text=chk_txt[i], font=my_font)
	chk.place(x=50, y=20 + (i * 35))

# ボタンクリックイベント(チェック初期値をセット)
def btn_click(bln):
	for i in range(len(chk_bln)):
		chk_bln[i].set(bln)

# ボタン作成
btn = tkinter.Button(tki, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
btn.place(x=40, y=210)
btn = tkinter.Button(tki, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
btn.place(x=40, y=252)
btn = tkinter.Button(tki, text="キャンセル", command=sys.exit, font=my_font)
btn.place(x=40, y=294)
btn = tkinter.Button(tki, text="実行", command=tki.destroy, font=my_font)
btn.place(x=40, y=336)

# イベントループ開始
tki.mainloop()

# チェック判定して展開
if chk_bln[0].get():
	# 秀丸メモ系
	open_dir = r'テキストファイルのフルパス'
	subprocess.Popen(['start', '/MAX', open_dir], shell=True)
if chk_bln[1].get():
	# Excel系
	open_dir = r'Excelファイルのフルパス'
subprocess.Popen(['start', '/MAX', open_dir], shell=True)
if chk_bln[2].get():
	# 一時的なメモ
	open_dir = r'メモ帳で開くファイルのフルパス'
	subprocess.Popen(['start', open_dir], shell=True)
if chk_bln[3].get():
	# フォルダ系
	open_dir = r'フォルダのフルパス'
	subprocess.Popen(['explorer', open_dir], shell=True)
if chk_bln[4].get():
	# プログラム系
	open_dir = r'プログラムのフルパス'
	subprocess.Popen([open_dir], shell=True)