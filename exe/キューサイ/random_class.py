import time
import pyautogui
import random



class Random_Class():
	def pag_random_click(self,element_obj,posi_offset_x,posi_offset_y):
		"""
		easeInQuad→最初を早く、最後を遅く
		easeOutQuad→最初を遅く、最後を早く
		easeInOutQuad→最初と最後を早く、道中は遅く
		easeInBounce→最後に跳ね返る
		easeInElastic→最後にゴムバンドのような動き
		"""

		# 要素ギリギリだとクリックできないことがあるのでこの分内側をクリックする
		set_pix=10
		# 新PCでは表示を1.5倍していたので要素のサイズも1.5倍する
		rand_width=random.randint(set_pix,element_obj.rect["width"]*1.5-set_pix)
		rand_height=random.randint(set_pix,element_obj.rect["height"]*1.5-set_pix)
		rand_duration=random.uniform(1,3)
		ease_list=[
			pyautogui.easeInQuad,
			pyautogui.easeOutQuad,
			pyautogui.easeInOutQuad,
			pyautogui.easeInBounce,
			pyautogui.easeInElastic,
		]
		rand_ease=random.choice(ease_list)
		func_list=[
			# 新PCでは表示を1.5倍していたので要素の座標も1.5倍する
			# posi_offset_x+element_obj.rect["x"]*1.5,
			# posi_offset_y+element_obj.rect["y"]*1.5,
			posi_offset_x+element_obj.rect["x"]*1.5+rand_width,
			posi_offset_y+element_obj.rect["y"]*1.5+rand_height,
			rand_duration,
			rand_ease
		]
		pyautogui.moveTo(*func_list)
		pyautogui.click()

	def random_sleep(self):
		random_sec=random.uniform(1,3)
		time.sleep(random_sec)
		return str(random_sec)+" 秒間スリープ"

# def test02():
# 	aaa=test_class01()
# 	bbb=aaa.random_sleep()
# 	print(bbb)
# test02()