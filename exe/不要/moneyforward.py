"""
2020年4月7日
iron更新したら画像検索できなくなったので対応した
ついでに、ファビコンクリックしてウィンドウアクティブ化して、メッセージボックスで実行するか聞くようにした

"""


import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
import tkinter
from tkinter import messagebox
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True
import time

"""
pyautogui.moveTo( 1, 1, 0 )
"""

ret = messagebox.askyesno('確認', 'マネーフォワードの画面を表示させた？')
ret = True
if ret == True:
	# マネフォのファビコンクリックしてウィンドウアクティブ化
	# region 反時計回りに範囲指定、始点を指定してそこから縦横範囲指定する感じ
	# 左上のx座標=1, 左上のy座標=1 の位置から幅1024, 高さ=30
	button_position = pyautogui.locateCenterOnScreen(r'C:\Users\YUTANAO\PycharmProjects\PythonScripts\exe\image\fabi.bmp', region=(1, 1, 1024, 30), confidence=0.95)
	pyautogui.click(button_position)
	pyautogui.press('home')
	time.sleep(1)

	while True:
		try:
			button_position = pyautogui.locateCenterOnScreen(r'C:\Users\YUTANAO\PycharmProjects\PythonScripts\exe\image\koushin.bmp', region=(200, 1, 45, 768), confidence=0.95)
			pyautogui.click( button_position )
		except ImageNotFoundException:
			try:
				button_position = pyautogui.locateCenterOnScreen(r'C:\Users\YUTANAO\PycharmProjects\PythonScripts\exe\image\end.bmp', region=(1, 660, 1024, 30), confidence=0.95)
				pyautogui.click(button_position)
				pyautogui.press('home')
				break
			except ImageNotFoundException:
				pyautogui.press('pagedown')
		time.sleep(0.5)
