# その他
import random
import time
import json
# selenium系
import pyautogui
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import configparser



# いいねした動画の辞書を返す
def tiktok_json_load():
	with open('TikTok_Data_1657155605/user_data.json','r',encoding='utf-8') as f:
		json_load=json.load(f)

		# 保存した音楽
		# ブラウザから保存する方法が分からなかったので保留
		FavoriteSoundList=json_load["Activity"]["Favorite Sounds"]["FavoriteSoundList"]

		# フォローされたアカウント
		FansList=json_load["Activity"]["Follower List"]["FansList"]

		# フォローしたアカウント
		Following=json_load["Activity"]["Following List"]["Following"]

		# 視聴履歴
		ShareHistoryList=json_load["Activity"]["Video Browsing History"]["VideoList"]

		# 保存した動画
		# 1つしか見れなかったのでそれだけいいねした
		FavoriteVideoList=json_load["Activity"]["Favorite Videos"]["FavoriteVideoList"]

		# いいねした動画
		ItemFavoriteList=json_load["Activity"]["Like List"]["ItemFavoriteList"]

		return ItemFavoriteList

# seleniumの設定
def selenium_driver():
	# chromedriver.exeのインストール先
	CDM_INST=ChromeDriverManager().install()
	# 起動時にオプションをつける
	# ポート指定により起動済みのブラウザのドライバーを取得
	chrome_options=webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
	return webdriver.Chrome(CDM_INST,options=chrome_options)

driver=selenium_driver()
posi_offset_x=driver.get_window_position()["x"]#+8
posi_offset_y=driver.get_window_position()["y"]#+80


# マウス操作
def pyautogui_random_click(element_obj,posi_offset_x,posi_offset_y):
	"""------------------------------
	easeInQuad→最初を早く、最後を遅く
	easeOutQuad→最初を遅く、最後を早く
	easeInOutQuad→最初と最後を早く、道中は遅く
	easeInBounce→最後に跳ね返る
	easeInElastic→最後にゴムバンドのような動き
	------------------------------"""
	set_pix=10
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
	pyautogui.doubleClick()
# ランダムにスリープ
def random_sleep():
	random_sec=random.uniform(1,3)
	time.sleep(random_sec)
	pri=str(random_sec)+" 秒間スリープ"
	return pri

def main01():
	while True:
		try:
			resume_flag=False

			config=configparser.ConfigParser()
			config.read('config.ini')
			resume_url=config['settings']['url']

			print(f"再開するURL:{resume_url}\n")

			# for count,i in enumerate(reversed(tiktok_json_load())):
			for count,i in enumerate(tiktok_json_load()):

				url=i["VideoLink"]
				print(f'count:{count} url:{url}')

				if resume_url==url or resume_url=='':
					resume_flag=True
				# print(f'resume_flag:{resume_flag}')

				if resume_flag==True:
					driver.get(url)
					time.sleep(1)

					# 404でも非公開アカウントでもなければ
					if ('404_face_icon' not in driver.page_source) and ('DivErrorContainer' in driver.page_source):
						# 動画のコンテナ要素をダブルクリック
						print('ダブルクリックした')
						webelement=driver.find_element_by_xpath("//div[contains(@class,'DivVideoControlContainer')]")
						webdriver.ActionChains(driver).double_click(webelement).perform()
					else:
						print(f"404_face_icon:{'404_face_icon' not in driver.page_source}")
						print(f"DivErrorContainer:{'DivErrorContainer' in driver.page_source}")

					# いいねした動画のURLを記録
					config.set('settings','url',url)
					with open('config.ini','w') as f:
						config.write(f)

		except:
			print(f'------------------------------')
			print(f'エラーが発生したため再試行')
			print(f'------------------------------')
			main01()

# エラーページでもpassしていいねしてURLを記録する
def main02():
	resume_flag=False

	config=configparser.ConfigParser()
	config.read('config.ini')
	resume_url=config['settings']['url']

	print(f"再開するURL:{resume_url}\n")

	for count,i in enumerate(reversed(tiktok_json_load())):
	# for count,i in enumerate(tiktok_json_load()):

		url=i["VideoLink"]
		print(f'count:{count} url:{url}')

		if resume_url==url or resume_url=='':
			resume_flag=True
		# print(f'resume_flag:{resume_flag}')

		if resume_flag==True:
			driver.get(url)
			time.sleep(1)

			# 404でも非公開アカウントでもなければ
			# chromeのタイトルを取得すればエラーページか判断可能
			try:
				# 動画のコンテナ要素をダブルクリック
				webelement=driver.find_element_by_xpath("//div[contains(@class,'DivVideoControlContainer')]")
				webdriver.ActionChains(driver).double_click(webelement).perform()
				print('ダブルクリックした')
			except:
				print('エラーページだけどpass')
				pass

			# いいねした動画のURLを記録
			config.set('settings','url',url)
			with open('config.ini','w') as f:
				config.write(f)

# エラーページでもpassしていいねしてURLを記録する
# 指定した回数いいねしたら終了する
def main03():
	resume_flag=False
	try_flag=True
	# いいねする回数
	like_limit=5

	config=configparser.ConfigParser()
	config.read('config.ini')

	resume_url=config['settings']['resume_url']
	print(f"resume_url:{resume_url}\n")
	try_count=int(config['settings']['try_count'])
	print(f"try_count:{try_count}\n")
	print("-"*30)

	for count,i in enumerate(reversed(tiktok_json_load())):
	# for count,i in enumerate(tiktok_json_load()):

		url=i["VideoLink"]
		print(f'パス {count} 個目のurl:{url}')

		# config.iniに記載されているurlが空なら最初から、forのurlと同じならそこから続きを行う
		if resume_url==url or resume_url=='':
			resume_flag=True
		# print(f'resume_flag:{resume_flag}')

		if resume_flag==True:
			# time.sleep(5)
			driver.get(url+'?is_copy_url=1&is_from_webapp=v1')
			time.sleep(1)

			# 404でも非公開アカウントでもなければ
			# chromeのタイトルを取得すればエラーページか判断可能
			try:
				# 動画のコンテナ要素をダブルクリック
				webelement=driver.find_element_by_xpath("//div[contains(@class,'DivVideoControlContainer')]")
				webdriver.ActionChains(driver).double_click(webelement).perform()
				try_count+=1
				print(f'{try_count} 個目 ダブルクリックした')
				# いいね出来たら加算
			except:
				print('エラーページだけどpass')
				pass

			# 最後に開いた動画のURLを記録
			# config.set('settings','resume_url',url)

			# 指定の個数いいねしたら終了
			if try_count>=like_limit:
				print(f'{like_limit} 個いいねしたので終了')
				config.set('settings','try_count','0')
				try_flag=False
			else:
				config.set('settings','try_count',str(try_count))

			# config.iniを更新
			# with open('config.ini','w') as f:
			# 	config.write(f)

			if try_flag==False: break

# いいねしたかを確認する
def main04():
	resume_flag=False
	try_flag=True
	# いいねする回数
	like_limit=5

	config=configparser.ConfigParser()
	config.read('config.ini')

	resume_url=config['settings']['resume_url']
	print(f"resume_url:{resume_url}\n")
	try_count=int(config['settings']['try_count'])
	print(f"try_count:{try_count}\n")
	print("-"*30)

	for count,i in enumerate(reversed(tiktok_json_load())):
		# for count,i in enumerate(tiktok_json_load()):

		url=i["VideoLink"]
		print(f'パス {count} 個目のurl:{url}')

		# config.iniに記載されているurlが空なら最初から、forのurlと同じならそこから続きを行う
		if resume_url==url or resume_url=='':
			resume_flag=True
		# print(f'resume_flag:{resume_flag}')

		if resume_flag==True:
			# time.sleep(5)
			driver.get(url+'?is_copy_url=1&is_from_webapp=v1')
			time.sleep(1)

			# 404でも非公開アカウントでもなければ
			# chromeのタイトルを取得すればエラーページか判断可能
			while True:
				try:
					# 動画のコンテナ要素をダブルクリック
					webelement=driver.find_element_by_xpath("//div[contains(@class,'DivVideoControlContainer')]")
					# webdriver.ActionChains(driver).double_click(webelement).perform()

					pyautogui_random_click(webelement,posi_offset_x,posi_offset_y)

					print(f'{try_count} 個目 ダブルクリックした')

					# ページ内に「LikeRedShadowColor_filter0_d」があればいいねされているのでbreak
					time.sleep(5)
					if 'LikeRedShadowColor_filter0_d' in driver.page_source:
						try_count+=1
						break
					else:
						print(f'いいねできていないのでリロードして再試行')
						driver.find_element_by_xpath("//div[contains(@class,'DivVideoControlContainer')]").send_keys(Keys.CONTROL,Keys.SHIFT,"r")
						# driver.refresh()
				# いいね出来たら加算
				except:
					print('エラーページだけどpass')
					pass

			# 最後に開いた動画のURLを記録
			# config.set('settings','resume_url',url)

			# 指定の個数いいねしたら終了
			if try_count>=like_limit:
				print(f'{like_limit} 個いいねしたので終了')
				config.set('settings','try_count','0')
				try_flag=False
			else:
				config.set('settings','try_count',str(try_count))

			# config.iniを更新
			# with open('config.ini','w') as f:
			# 	config.write(f)

			if try_flag==False: break


# main01()
# main02()
# main03()
main04()