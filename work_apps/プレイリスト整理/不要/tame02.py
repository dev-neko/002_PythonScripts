import shutil
import bs4
import os
import pathlib
from mutagen.easyid3 import EasyID3



# HTMLを基にファイルを移動させるバージョン



bs4obj = bs4.BeautifulSoup(open('抽出したプレイリスト.html', encoding='utf-8'), 'html.parser')

for a in bs4obj.find_all("div",attrs={'class':'folder-name'}):
	# os.mkdir('プレイリスト/'+a.find("h3").text)
	p_name=a.find("h3").text
	for b in a.find_all("div",attrs={'class':'file-name'}):
		f_name=b.text
		for c in os.listdir('トラック'):
			print("プレイリストの曲名：",f_name.replace(".csv",""))
			print("トラックフォルダーのタイトル：",EasyID3('トラック/'+c)["title"])
			if f_name.replace(".csv","") in EasyID3('トラック/'+c)["title"]:
				print("\t"+p_name," に ",c," を移動")
				# shutil.move('トラック/'+c,'プレイリスト/'+p_name)
				break
	# break