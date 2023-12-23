import subprocess
import tkinter.font
import sys
# from my_module import my_function



# ボタンクリックイベント(チェック初期値をセット)
def btn_click(bln):
	for i in range(len(chk_bln)):
		chk_bln[i].set(bln)



# Tkクラス生成
root = tkinter.Tk()
# 画面サイズ
root.geometry()
# 画面タイトル
root.title('アーカイブを作成するノートブックの選択')

# フォントオブジェクトを新規に作成
my_font = tkinter.font.Font(root,family='BIZ UDゴシック',size=12)

# Frameを設定
frame=tkinter.Frame(root)

label = tkinter.Label(root, text='アーカイブを作成するノートブックを選択してください。')

# チェックボタンのラベルをリスト化する
chk_txt=["【済】Coaching Free Salon(CFS)","【済】ha-monヒーリングサロン","【済】Healing Online Salon(HOS)","【済】週刊CFS","【済】週刊HOS","【済ヒーリング】連続遠隔ヒーリング","【済】特別儀式／鑑定"]
# チェックボックスON/OFFの状態
chk_bln = {}
# チェックボタンを動的に作成して配置
for i in range(len(chk_txt)):
	chk_bln[i] = tkinter.BooleanVar()
	chk = tkinter.Checkbutton(root, variable=chk_bln[i], text=chk_txt[i], font=my_font)
	chk.place(x=20, y=20 + (i * 35))

# ボタン作成
btn = tkinter.Button(root, text='全てにチェックを入れる', command=lambda:btn_click(True), font=my_font)
btn.place(x=40, y=230)
btn = tkinter.Button(root, text='全てのチェックを外す', command=lambda:btn_click(False), font=my_font)
btn.place(x=20, y=272)
btn = tkinter.Button(root, text="実行", command=root.destroy, font=my_font, width=45)
btn.place(x=0, y=314)
btn = tkinter.Button(root, text="終了", command=sys.exit, font=my_font)
btn.place(x=40, y=356)

# イベントループ開始
root.mainloop()

# チェック判定して展開
if chk_bln[0].get():
	pass