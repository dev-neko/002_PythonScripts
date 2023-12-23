import re
import shutil
import bs4
import os
import pathlib
from mutagen.easyid3 import EasyID3



# ファイルを基にHTMLを検索してファイルを移動させるバージョン



bs4obj = bs4.BeautifulSoup(open('抽出したプレイリスト.html', encoding='utf-8'), 'html.parser')


def tame01():
	for track_f_name in os.listdir('トラック'):
		print("ファイル名：",track_f_name)
		for html_f_name_obj in bs4obj.find_all("div",attrs={'class':'file-name'}):
			html_f_name=html_f_name_obj.text.replace(".csv","")
			print("HTMLの曲名：",html_f_name)
			html_p_name=html_f_name_obj.parent.find("h3").text
			if html_f_name in re.sub(r'[\\/:*?"<>|%]','_',EasyID3('トラック/'+track_f_name)["title"][0]):
				print("\t",html_p_name," に ",track_f_name," を移動")
				break
# tame01()


def tame03():
	# track_dir='トラック'
	track_dir=r'C:\Users/YUTANAO/Documents/在宅仕事/jin21様/トラック/'
	list_len=len(os.listdir(track_dir))
	for count,track_f_name in enumerate(os.listdir(track_dir)):
		track_t_name=EasyID3(track_dir+track_f_name)["title"][0]
		# print("ファイル名：",track_f_name)
		# print("タイトル名：",track_t_name)
		print(count,"/",list_len)
		for html_f_name_obj in bs4obj.find_all("div",attrs={'class':'file-name'}):
			html_f_name=html_f_name_obj.text.replace(".csv","")
			# print("HTMLの曲名：",html_f_name)
			html_p_name=html_f_name_obj.parent.find("h3").text
			if html_f_name==re.sub(r'[\\/:*?"<>|%]','_',track_t_name):
				print(html_p_name,"に",track_f_name,"を移動")
				shutil.move(track_dir+track_f_name,'プレイリスト/'+html_p_name)
				break
		if os.path.isfile(track_dir+track_f_name):
			print(track_t_name,"は該当無しに移動")
			shutil.move(track_dir+track_f_name,'該当なし')
tame03()
