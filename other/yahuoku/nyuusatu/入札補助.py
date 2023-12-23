"""
2020年5月27日
"""

import keyboard
import pyautogui
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
alrbid_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\alrbid.png"

while True:
	print("入力待ち…")
	if keyboard.read_event().event_type==keyboard.KEY_DOWN:
		# print(keyboard.read_event().name)
		if keyboard.read_event().name=="home":
			# ------------------------------
			while True:
				py_bt = my_function.LCOS(bid_dir,780,0,880,768)
				if py_bt != False:
					pyautogui.click(py_bt)
					break
				else:
					print("bid.png が見つからない")
				time.sleep(0.1)
			# ------------------------------
			while True:
				if my_function.LCOS(conf_dir,450,0,560,768) != False:
					pyautogui.click(my_function.LCOS(conf_dir,450,0,560,768))
					break
				elif my_function.LCOS(kosuu_dir,360,0,560,768) != False:
					pyautogui.click(my_function.LCOS(kosuu_dir,360,0,560,768))
					break
				else:
					print("conf.png または kosuu.png が見つからない")
				time.sleep(0.1)
			# ------------------------------
			while True:
				if my_function.LCOS(bidconf_dir,450,0,550,768) != False:
					pyautogui.click(my_function.LCOS(bidconf_dir,450,0,550,768))
					break
				else:
					print("bidconf.png が見つからない")
				time.sleep(0.1)
			# ------------------------------
			while True:
				if (my_function.LCOS(end_dir,320,300,500,340) != False or
					my_function.LCOS(alrbid_dir,55,0,280,768) != False):
					pyautogui.hotkey('ctrl', 'w')
					break
				else:
					print("end.png、alrbid.png が見つからない")
				time.sleep(0.1)
			# ------------------------------
