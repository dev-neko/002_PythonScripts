import time
import keyboard
import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION=True


bid_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\bid.png"
conf_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\conf.png"
bidconf_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\bidconf.png"
end_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\end.png"
kosuu_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\kosuu.png"
seigen_dir = r"C:\Users\YUTANAO\PycharmProjects\PythonScripts\yahuoku\nyuusatu\seigen.png"

while True:
	try:
		py_bt=pyautogui.locateCenterOnScreen(conf_dir,region=(450,470,100,50),
																					 confidence=0.95)
		pyautogui.click(py_bt)
		break
	except ImageNotFoundException:
		print("conf.png が見つからない")
		try:
			py_bt=pyautogui.locateCenterOnScreen(kosuu_dir,region=(340,390,50,30),
																					 confidence=0.95)
			pyautogui.click(py_bt)
			break
		except ImageNotFoundException:
			print("kosuu.png が見つからない")
	time.sleep(0.5)
