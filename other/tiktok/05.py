import time
import json

# selenium系
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

# aaa
def selenium_driver():
	# chromedriver.exeのインストール先
	CDM_INST=ChromeDriverManager().install()

	# 起動時にオプションをつける
	# ポート指定により起動済みのブラウザのドライバーを取得
	chrome_options=webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
	driver=webdriver.Chrome(CDM_INST,options=chrome_options)

	return driver


driver=selenium_driver()


def main():
	while True:
		try:
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
			main()


main()