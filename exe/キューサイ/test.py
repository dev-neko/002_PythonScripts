def test01():
	import datetime

	JST=datetime.timezone(datetime.timedelta(hours=9),'JST')
	# 12時間制+AM/PM+曜日
	d=datetime.datetime.now(JST).strftime('%Y/%m/%d(%a) (%p)%I:%M')
	print(d)
# test01()

import time
import pyautogui
import random
class test_class01():
	def pyautogui_random_click(self,element_obj,posi_offset_x,posi_offset_y):
		"""
		easeInQuad→最初を早く、最後を遅く
		easeOutQuad→最初を遅く、最後を早く
		easeInOutQuad→最初と最後を早く、道中は遅く
		easeInBounce→最後に跳ね返る
		easeInElastic→最後にゴムバンドのような動き
		"""
		set_pix=8
		rand_width=random.randint(set_pix,element_obj.rect["width"]-set_pix)
		rand_height=random.randint(set_pix,element_obj.rect["height"]-set_pix)
		rand_duration=random.uniform(0.5,3)
		# ease_list=[pyautogui.easeInQuad,pyautogui.easeOutQuad,pyautogui.easeInOutQuad,pyautogui.easeInBounce,pyautogui.easeInElastic]
		ease_list=[pyautogui.easeInQuad,pyautogui.easeOutQuad,pyautogui.easeInOutQuad]
		rand_ease=ease_list[random.randint(0,2)]
		func_list=[element_obj.rect["x"]+rand_width+posi_offset_x,
							 element_obj.rect["y"]+rand_height+posi_offset_y,
							 rand_duration,
							 rand_ease]
		pyautogui.moveTo(*func_list)
		pyautogui.click()

	def random_sleep(self):
		random_sec=random.uniform(1,3)
		time.sleep(random_sec)
		return str(random_sec)+" 秒間スリープ"

def test02():
	aaa=test_class01()
	bbb=aaa.random_sleep()
	print(bbb)
# test02()

