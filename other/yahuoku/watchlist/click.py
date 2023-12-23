"""
2020年5月22日
とりあえずクリックできるようになったけど、実際はそんなに量多くないので使わないかも
↓ここ参考にした
https://winzu44.hatenablog.com/entry/2020/04/09/215321
"""
import keyboard
import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
import tkinter
from tkinter import messagebox
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION=True
import time


watch_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\watchlist\watch_icon.png"
footer_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\watchlist\footer.png"
next_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\watchlist\next.png"

while True:
	try:
		# locateAllOnScreen で一致した画像の座標をすべて取得
		for pos in pyautogui.locateAllOnScreen(watch_dir, confidence=0.950):
			# center で中央座標取得
			cpos = pyautogui.center(pos)
			pyautogui.moveTo(cpos)
			# キーボードのボタンが押されるまで待つ
			if keyboard.read_event().event_type==keyboard.KEY_DOWN:
				# 押されたボタンが右ボタンなら画像の座標をクリック、それ以外は何もしない
				if keyboard.read_event().name == "right":
					pyautogui.click(cpos)
		# for が終了したら次へボタンあったらクリックして、無ければページダウンさせて再度画像検出
		try:
			fopos = pyautogui.locateCenterOnScreen(footer_dir, confidence=0.95)
			pyautogui.moveTo(fopos)
			nepos = pyautogui.locateCenterOnScreen(next_dir,confidence=0.95)
			pyautogui.click(nepos)
		except ImageNotFoundException:
			pyautogui.press('pagedown')
	# 画像が検出できなかったらページダウンさせて再度画像検出
	except ImageNotFoundException:
		try:
			fopos = pyautogui.locateCenterOnScreen(footer_dir, confidence=0.95)
			pyautogui.moveTo(fopos)
			nepos = pyautogui.locateCenterOnScreen(next_dir,confidence=0.95)
			pyautogui.click(nepos)
		except ImageNotFoundException:
			pyautogui.press('pagedown')
	time.sleep(0.5)

