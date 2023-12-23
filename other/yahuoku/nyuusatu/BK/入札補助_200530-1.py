"""
2020年5月27日
"""

import keyboard
import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
import tkinter
from tkinter import messagebox
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION=True
import time
from my_module import my_function



"""
入札時は
m8eV3MOvx5JJrBs@yahoo.co.jp
X|fUYZ#b[4
を使う
"""

bid_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\bid.png"
conf_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\conf.png"
bidconf_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\bidconf.png"
end_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\end.png"
kosuu_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\kosuu.png"
seigen_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\seigen.png"

while True:
	if keyboard.read_event().event_type==keyboard.KEY_DOWN:
		# print(keyboard.read_event().name)
		if keyboard.read_event().name=="home":
			while True:
				try:
					py_bt = pyautogui.locateCenterOnScreen(bid_dir, region=(780, 0, 100, 768),
																									confidence=0.95)
					pyautogui.click(py_bt)
					break
				except ImageNotFoundException:
					print("bid.png が見つからない")
					pyautogui.press('home')
				time.sleep(0.5)
			while True:
				try:
					if pyautogui.locateCenterOnScreen(conf_dir, region=(450, 470, 100, 50),confidence=0.95):
						py_bt = pyautogui.locateCenterOnScreen(conf_dir, region=(450, 470, 100, 50),
																										confidence=0.95)
						pyautogui.click(py_bt)
						break
					elif pyautogui.locateCenterOnScreen(kosuu_dir, region=(340, 390, 50, 30),
																								confidence=0.95):
						break
				except ImageNotFoundException:
					print("conf.png または kosuu.png が見つからない")
				time.sleep(0.5)
			while True:
				try:
					if pyautogui.locateCenterOnScreen(bidconf_dir, region=(450, 0, 100, 768),
																									confidence=0.95):
						py_bt = pyautogui.locateCenterOnScreen(bidconf_dir, region=(450, 0, 100, 768),
																									confidence=0.95)
						pyautogui.click(py_bt)
						break
					elif pyautogui.locateCenterOnScreen(seigen_dir, region=(170, 270, 670, 50),
																									confidence=0.95):
						pyautogui.hotkey('ctrl','w')
						break
				except ImageNotFoundException:
					print("bidconf.png が見つからない")
				time.sleep(0.5)
			while True:
				try:
					py_bt = pyautogui.locateCenterOnScreen(end_dir, region=(320, 300, 180, 40),
																									confidence=0.95)
					pyautogui.hotkey('ctrl', 'w')
					break
				except ImageNotFoundException:
					print("end.png が見つからない")
				time.sleep(0.5)
