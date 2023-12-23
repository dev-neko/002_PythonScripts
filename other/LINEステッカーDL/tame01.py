"""
使い方

そのまま実行すればExcelでコピペしやすいような形でクリップボードにコピーされる
"""


import bs4
import pyperclip
import requests
import datetime
import jpholiday
import smtplib
from email.mime.text import MIMEText


# URLからソースを取得
ipo_url = "https://store.line.me/stickershop/product/10121827/ja"
get_url_parser = requests.get(ipo_url)
get_url_parser.encoding = 'utf-8'
bs4obj = bs4.BeautifulSoup(get_url_parser.text,'html.parser')
print(bs4obj)

# 銘柄ごとの詳細URL取得
for detail_url in reversed(bs4obj.find_all("h2",attrs={'class':'h2_ipolist_name'})):
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
		# 上場日 取得
		update = bs4obj_detail_url.find_all("td",attrs={'class':'main_data aligncenter'})[4].text
		# 公開株数 取得
		kabusuu = bs4obj_detail_url.find_all("td",attrs={'class':'main_data alignright'})[0].text
		# 公募価格 無ければ 仮条件 無ければ 仮条件提示日 取得
		# 公募価格 取得
		koubo = bs4obj_detail_url.find("td",attrs={'class':'main_data alignright','colspan':'4'}).text
		# 仮条件 取得
		karijouken = bs4obj_detail_url.find_all("td",attrs={'class':'main_data alignright'})[8].text
		# 仮条件提示日 取得
		karijouken_teiji = bs4obj_detail_url.find_all("td",attrs={'class':'main_data','colspan':'4'})[0].text
		if "\xa0" != koubo:
			kakaku = koubo
		elif "\xa0" != karijouken:
			kakaku = karijouken
			kakaku = kakaku[kakaku.find('〜')+1:]
		else:
			kakaku = karijouken_teiji
		kakaku=kakaku.replace(",","")
		kakaku=kakaku.replace("円","")
		kakaku=kakaku.replace("2020/0","")
		kakaku=kakaku.replace("2020/","")
		# ブックビルディング(開始) 取得
		bb_str = bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[16].text
		# ブックビルディング(終了) 取得
		bb_end = bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[17].text

		# 幹事団取得
		# 主幹事を1つ前の証券会社名と比較して除外するバージョン
		"""
		kanji_list = []
		kanji=""
		for fo_kanji in bs4obj_detail_url.find_all("td",attrs={'class':'main_data'}):
			kanji_text = fo_kanji.text
			kanji_text = kanji_text.replace("\xa0", "")
			kanji_text = kanji_text.replace(" ","")
			# <td class="main_data"> でしか抽出できないので証券か證券が入っていれば幹事団と判断
			# →これだと
			if ("証券" in kanji_text) or ("證券" in kanji_text):
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
		"""
		# "\xa0"が含まれていたら主幹事と判断して除外するバージョン
		kanji_list = []
		kanji=""
		for fo_kanji in bs4obj_detail_url.find_all("td",attrs={'class':'main_data'}):
			kanji_text = fo_kanji.text
			# <td class="main_data"> でしか抽出できないので証券か證券が入っていてれば幹事団と判断
			# "\xa0"が入っている場合は主幹事なので除外
			# これだと 野村證券(株)入社 ドレスナークラインオートベンソン証券会社入社
			# とかも幹事になっちゃうのでとりあえず"入社"で除外した
			if (("証券" in kanji_text) or ("證券" in kanji_text))\
				and ("\xa0" not in kanji_text) and ("入社" not in kanji_text):
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

		# Excelでコピペしやすいように整理

		# 銘柄名
		# ipo_name
		# 上場日
		# update
		# 公開株数
		# kabusuu
		# 公募価格 or 仮条件 or 仮条件提示日
		# kakaku
		# ブックビルディング(開始)
		# bb_str
		# ブックビルディング(終了)
		# bb_end
		# 抽選日
		# bb_kekka
		# 幹事団
		# kanji_list

		# BB終了日から抽選日が平日になる日付を求める
		# +1日だと結果出てない場合が多いので+2にした
		bb_end_rep=bb_end.replace("/","")
		bb_end_p2=datetime.date(int(bb_end_rep[0:4]),int(bb_end_rep[4:6]),int(bb_end_rep[6:8]))+datetime.timedelta(days=2)
		while True:
			if isHoliDay(bb_end_p2.strftime('%Y%m%d')):
				pass
			else:
				bb_kekka = bb_end_p2.strftime('%Y/%m/%d')
				break
			bb_end_p2=bb_end_p2+datetime.timedelta(days=1)

		# Excelでコピペしやすいようにタブ付加して結合
		excel_data = excel_data + ipo_name+"\t"+bb_str+"\t"+bb_end+"\t"+bb_kekka+"\t"+kakaku
		# +=だと配列でまとめて末尾にそれぞれ1つの要素として結合される
		excel_data_list = []
		excel_data_list += [ipo_name+"\t",bb_str,"\t"+bb_end,"\t"+bb_kekka,"\t"+kakaku]

		# 幹事団まとめ
		for count, fo_kanji_list in enumerate(kanji_list):
			# 13で割り切れれば、改行文字+タブ文字5個にする、0を割ると余り0になるので+1した
			if (count+1) % 13 == 0:
				excel_data = excel_data + "\n\t\t\t\t\t" + fo_kanji_list
				excel_data_list.append("\n\t\t\t\t\t" + fo_kanji_list)
			else:
				excel_data = excel_data +"\t"+ fo_kanji_list
				excel_data_list.append("\t"+ fo_kanji_list)

		excel_data = excel_data + "\n"
		excel_data_list.append("\n")
		mail_data.append(excel_data_list)

# print(mail_data[0][1])
# print(mail_data[1][1])
print(mail_data)

# for fa in mail_data:
# 	print(fa[1])

# print(excel_data)
pyperclip.copy(excel_data)
# send_mail("IPOデータ",excel_data)

		# break
