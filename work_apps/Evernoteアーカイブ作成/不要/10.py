import tkinter.font
from tkinter import *
import sys





def cre_tkinter(title_in,title_not_in):
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
	root.title('Evernote整理アプリ')

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
	my_font = font.Font(root,family='BIZ UDゴシック',size=12)

	label = Label(frame_label, text='アーカイブを作成するノートブック名を選択してください。')
	label.grid()

	# チェックボタンのラベルをリスト化する
	chk_txt=title_in+title_not_in
	# チェックボックスON/OFFの状態
	chk_bln = {}
	# チェックボタンを動的に作成して配置
	for i in range(len(chk_txt)):
		chk_bln[i] = BooleanVar(value=True)
		chk = Checkbutton(frame_chk, variable=chk_bln[i], text=chk_txt[i], font=my_font)
		chk.grid(sticky=W)

	# ボタン作成
	btn = Button(frame_btn, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text="実行", command=root.destroy, font=my_font)
	btn.pack(expand=True,fill=tkinter.X)
	btn = Button(frame_btn, text="終了", command=sys.exit, font=my_font)
	btn.pack(expand=True,fill=tkinter.X)

	# イベントループ開始
	root.mainloop()

	# チェックを入れたテキストを配列に入れる
	return_list=[]
	for i in range(len(chk_bln)):
		if chk_bln[i].get(): return_list.append(chk_txt[i])

	return return_list

title_in=["【済】Coaching Free Salon(CFS)","【済】ha-monヒーリングサロン","【済】Healing Online Salon(HOS)","【済】週刊CFS","【済】週刊HOS","【済ヒーリング】連続遠隔ヒーリング"]
title_not_in=["【済】特別儀式／鑑定"]
tk_chk_list=cre_tkinter(title_in,title_not_in)
print(tk_chk_list)