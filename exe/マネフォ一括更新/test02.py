"""
2020年4月7日
iron更新したら画像検索できなくなったので対応した
ついでに、ファビコンクリックしてウィンドウアクティブ化して、メッセージボックスで実行するか聞くようにした

2022年5月20日
PCを新調したので調整した

2022年10月1日
PC再起動したからなのか更新画像が反応しなかったので撮り直した
"""


import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True
import time


"""
pyautogui.moveTo( 1, 1, 0 )
# マネフォのファビコンクリックしてウィンドウアクティブ化
# region 反時計回りに範囲指定、始点を指定してそこから縦横範囲指定する感じ
# 左上のx座標=1, 左上のy座標=1 の位置から幅1024, 高さ=30
"""

# スクリプトの絶対パス
dir=r'C:\Users\YUTAKA\PycharmProjects\PythonApps\002_PythonScripts\exe\マネフォ一括更新'

while True:
	try:
		button_position=pyautogui.locateCenterOnScreen(dir+r'\end.bmp',grayscale=True)
		pyautogui.click(button_position)
	except ImageNotFoundException:
		pass
	time.sleep(1)