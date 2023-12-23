"""
使い方
	そのまま実行すればExcelでコピペしやすいような形で出力される

2020年7月4日
	とりあえず取得した情報取得できるようになった
2020年7月6日
	幹事団を取得できるようになった
	幹事団はリストに入れるときに少し難しそうなところで終了
2020年7月8日
	幹事団はリストに入れて取得したらすぐにprintさせれば2次元配列に入れずに、表示させたら初期化させれば
	2次元配列使う必要ない
	その他の銘柄名などはそもそもリストにする必要も無さそうだったので、一応BK作って変更した
	001.pyはそこまでで終了

次回やる事
	幹事団取得
	Excelで取り込みやすいように、必要な情報だけコピペできるように整形する
	Excelを取り込みやすい形に変える→第2期
"""


import bs4
import requests
import numpy


# 銘柄名
ipo_name_list = []
# 上場日
update_list = []
# 公開株数
kabusuu_list = []
# 公募価格 or 仮条件 or 仮条件提示日
kakaku_list = []
# ブックビルディング(開始)
bb_str_list = []
# ブックビルディング(終了)
bb_end_list = []
# 幹事団
kanji_list = []


# URLからソースを取得
ipo_url = "http://www.tokyoipo.com/ipo/schedule.php"
get_url_parser = requests.get(ipo_url)
get_url_parser.encoding = 'EUC-JP'
bs4obj = bs4.BeautifulSoup(get_url_parser.text,'html.parser')
# print(bs4obj)

# 銘柄ごとの詳細URL取得
for detail_url in bs4obj.find_all("h2",attrs={'class':'h2_ipolist_name'}):
	detail_url = detail_url.find("a").get('href')
	# preとpostで別れているので、preの場合だけその銘柄の詳細ページのソース取得
	if "post" not in detail_url:
		detail_url_parser=requests.get("http://www.tokyoipo.com"+detail_url)
		detail_url_parser.encoding='EUC-JP'
		bs4obj_detail_url=bs4.BeautifulSoup(detail_url_parser.text,'html.parser')
		# 銘柄名 取得
		ipo_name = bs4obj_detail_url.find("h1",attrs={'class':'h1_title_ipodata'}).text
		ipo_name = ipo_name.replace("（株）","")
		ipo_name = ipo_name.replace("\u3000", " ")
		ipo_name_list.append(ipo_name)
		# 上場日 取得
		update_list.append(bs4obj_detail_url.find_all("td",attrs={'class':'main_data aligncenter'})[4].text)
		# 公開株数 取得
		kabusuu_list.append(bs4obj_detail_url.find_all("td",attrs={'class':'main_data alignright'})[0].text)
		# 公募価格 無ければ 仮条件 無ければ 仮条件提示日 取得
		# 公募価格 取得
		koubo = bs4obj_detail_url.find("td",attrs={'class':'main_data alignright','colspan':'4'}).text
		# 仮条件 取得
		karijouken = bs4obj_detail_url.find_all("td",attrs={'class':'main_data alignright'})[8].text
		# 仮条件提示日 取得
		karijouken_teiji = bs4obj_detail_url.find_all("td",attrs={'class':'main_data','colspan':'4'})[0].text
		if "\xa0" != koubo:
			kakaku_list.append(koubo)
		elif "\xa0" != karijouken:
			kakaku_list.append(karijouken)
		else:
			kakaku_list.append(karijouken_teiji)
		# ブックビルディング(開始) 取得
		bb_str_list.append(bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[16].text)
		# ブックビルディング(終了) 取得
		bb_end_list.append(bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[17].text)

		# print(ipo_name_list,
		# 			update_list,
		# 			kabusuu_list,
		# 			kakaku_list,
		# 			bb_str_list,
		# 			bb_end_list)

		# 幹事団取得
		# 銘柄名の取得数で2次元配列の列？を決める
		# kanji_list =

		kanji=""
		for fo_kanji in bs4obj_detail_url.find_all("td",attrs={'class':'main_data'}):
			kanji_text = fo_kanji.text
			kanji_text = kanji_text.replace("\xa0", "")
			kanji_text = kanji_text.replace(" ","")
			if "証券" in kanji_text or "證券" in kanji_text:
				kanji_juu = kanji_text
				if kanji != kanji_text:
					kanji_text = kanji_text.replace("証券","")
					kanji_text = kanji_text.replace("證券","")
					if "ＳＭＢＣ日興" == kanji_text:
						kanji_list.append("ユSM")
						kanji_list.append("ナSM")
					elif "三菱ＵＦＪモルガン・スタンレー" == kanji_text:
						kanji_list.append("ユモル")
						kanji_list.append("ナモル")
					elif kanji_text in "いちよし、マネックス、みずほ、岩井コスモ、東海東京":
						kanji_list.append("ユ"+kanji_text[0:2])
						kanji_list.append("ナ"+kanji_text[0:2])
					elif kanji_text in "エース、極東、西日本シティTT、":
						pass
					else:
						kanji_list.append("ユ"+kanji_text)
						kanji_list.append("ナ"+kanji_text)
				kanji = kanji_juu
		print(kanji_list)
		print("------------------------------")





		break





# Excelでコピペしやすいように整理

