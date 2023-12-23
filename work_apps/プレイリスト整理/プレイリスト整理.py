import pathlib
import pprint
import re
import shutil
import subprocess
import sys
import time

import bs4
import os
import xlwings
from mutagen.easyid3 import EasyID3
import tqdm



base_bir=r"C:/Users/YUTANAO/Documents/在宅仕事\jin21様/プレイリスト整理/"
track_dir=base_bir+"トラック/"
play_dir=base_bir+"プレイリスト/"
nofind_dir=base_bir+"該当なし/"

bs4obj = bs4.BeautifulSoup(open(base_bir+'抽出したプレイリスト.html', encoding='utf-8'), 'html.parser')

Excel='プレイリスト整理.xlsx'
wb=xlwings.Book(Excel)



"""
プレイリストフォルダ作成
"""
def tame01():
	pbar=tqdm.tqdm(bs4obj.find_all("h3"))
	for a in pbar:
		os.mkdir(play_dir+a.text)
# tame01()


"""
ExcelにHTMLのタイトル、プレイリスト名を記載する
"""
def tame07():
	sht_1=wb.sheets['1']

	html_title_name_obj=bs4obj.find_all("div",attrs={'class':'file-name'})

	for count,html_title_name_obj in enumerate(tqdm.tqdm(html_title_name_obj)):
		# 書き込み
		sht_1.range(count+2,1).value=html_title_name_obj.parent.find("h3").text
		sht_1.range(count+2,2).value=html_title_name_obj.text

	wb.save()
# tame07()


"""
Excelのシート2に、ファイル名、47文字、.mp3削除→47文字、スぺ削除→47文字 の内容をExcelに記載する
"""
def tame09():
	sht_2=wb.sheets['2']

	track_file_name_list=os.listdir(track_dir)
	# track_file_name_list_len=len(track_file_name_list)
	# 半角全角スペースを削除するテーブル
	tr_table=str.maketrans({'　':'',' ':'',})

	pbar=tqdm.tqdm(track_file_name_list)
	for count,track_file_name in enumerate(pbar):
		# pbar.set_description(f'{count+1}/{track_file_name_list_len}')

		track_title_name=EasyID3(track_dir+track_file_name)["title"][0][:47]
		track_title_name_mp3=EasyID3(track_dir+track_file_name)["title"][0].replace(".mp3","")[:47]
		track_title_name_space=EasyID3(track_dir+track_file_name)["title"][0].translate(tr_table)[:47]

		# HTMLのタイトルはcsvのファイル名なので、ファイル名に使えない文字は置換する
		track_title_name_sub=re.sub(r'[\\/&:*\'?"<>|%;]','_',track_title_name)
		track_title_name_mp3_sub=re.sub(r'[\\/&:*\'?"<>|%;]','_',track_title_name_mp3)
		track_title_name_space_sub=re.sub(r'[\\/&:*\'?"<>|%;]','_',track_title_name_space)

		sht_2.range(count+2,1).value=track_file_name
		sht_2.range(count+2,2).value=track_title_name_sub
		sht_2.range(count+2,3).value=track_title_name_mp3_sub
		sht_2.range(count+2,4).value=track_title_name_space_sub
# tame09()


"""
大体整理できたので、まず、HTMLを元にして、音楽ファイルが存在するかを確認する
同時に該当する音楽ファイルのファイル名をExcelに記載する

先にシート2に、ファイル名、47文字、.mp3削除→47文字、スぺ削除→47文字 の内容をExcelに記載する
を利用するバージョン
"""
def tame10():
	sht_1=wb.sheets['1_一致無し抽出']
	sht_2=wb.sheets['2']

	if sht_1.range(2,3).value==None:
		file_name_str=sht_1.range(1,3)
	else:
		file_name_str=sht_1.range(1,3).end("down")

	# 比較するタイトルをリストで取得
	track_file_name_list=sht_2.range(2,1).expand("down").value
	track_title_name_sub_list=sht_2.range(2,2).expand("down").value
	track_title_name_mp3_sub_list=sht_2.range(2,3).expand("down").value
	track_title_name_space_sub_list=sht_2.range(2,4).expand("down").value

	# HTMLのタイトルをリストで取得
	html_title_name_list=file_name_str.offset(1,-1).expand("down").value
	# HTMLのタイトル数を取得
	html_title_name_list_len=len(html_title_name_list)
	# 半角全角スペースを削除するテーブル
	tr_table=str.maketrans({'　':'',' ':'',})

	# プログレスバー宣言
	pbar=tqdm.tqdm(html_title_name_list)
	for count1,html_title_name in enumerate(pbar):
		pbar.set_description(f'{count1+1}/{html_title_name_list_len}')
		# HTMLの .csv を取り除いたタイトル名
		html_title_name_csv=html_title_name.replace(".csv","")
		# HTMLの .mp3.csv を取り除いたタイトル名
		html_title_name_mp3csv=html_title_name.replace(".mp3.csv","")
		# HTMLの .m4a.csv を取り除いたタイトル名
		html_title_name_m4acsv=html_title_name.replace(".m4a.csv","")

		# 全てに一致しなかったカウンタ
		no_find_c=True
		for (track_file_name,
				 track_title_name_sub,
				 track_title_name_mp3_sub,
				 track_title_name_space_sub) in zip(track_file_name_list,
																						track_title_name_sub_list,
																						track_title_name_mp3_sub_list,
																						track_title_name_space_sub_list):

			if track_title_name_sub==html_title_name_csv or \
				track_title_name_sub==html_title_name_mp3csv or \
				track_title_name_sub==html_title_name_m4acsv:
				file_name_str.offset(count1+1,1).value='47文字'
				no_find_c=False
			elif track_title_name_mp3_sub==html_title_name_csv or \
				track_title_name_mp3_sub==html_title_name_mp3csv or \
				track_title_name_mp3_sub==html_title_name_m4acsv:
				file_name_str.offset(count1+1,1).value='.mp3削除→47文字'
				no_find_c=False
			elif track_title_name_space_sub==html_title_name_csv.translate(tr_table) or \
				track_title_name_space_sub==html_title_name_mp3csv.translate(tr_table) or \
				track_title_name_space_sub==html_title_name_m4acsv.translate(tr_table):
				file_name_str.offset(count1+1,1).value='スぺ削除→47文字'
				no_find_c=False
			if no_find_c==False:
				file_name_str.offset(count1+1,0).value=track_file_name
				break
		if no_find_c:
			file_name_str.offset(count1+1,0).value='一致無し'
# tame10()


"""
ファイル名には(1)とかが付いてるけどタイトル名には付いていない。大体同じタイトルの物が2つ以上ある。→タイトルに同じ()の内容があれば同一と判断
だけに対応したバージョン
"""
def tame11():
	# ()に対する正規表現
	pare_com=re.compile(r'\(.*?\)')

	sht_1=wb.sheets['1_一致無し抽出']
	sht_2=wb.sheets['2']

	file_name_str=sht_1.range(1,3)

	# 比較するタイトルをリストで取得
	track_file_name_list=sht_2.range(2,1).expand("down").value
	track_title_name_sub_list=sht_2.range(2,2).expand("down").value
	track_title_name_mp3_sub_list=sht_2.range(2,3).expand("down").value
	track_title_name_space_sub_list=sht_2.range(2,4).expand("down").value

	# HTMLのタイトルをリストで取得
	html_title_name_list=file_name_str.offset(1,-1).expand("down").value
	# HTMLのタイトル数を取得
	html_title_name_list_len=len(html_title_name_list)
	# 半角全角スペースを削除するテーブル
	tr_table=str.maketrans({'　':'',' ':'',})

	# プログレスバー宣言
	# pbar=tqdm.tqdm(html_title_name_list)
	for count1,html_title_name in enumerate(html_title_name_list):
		# pbar.set_description(f'{count1+1}/{html_title_name_list_len}')
		# HTMLの .csv を取り除いたタイトル名
		html_title_name_csv=html_title_name.replace(".csv","")
		# HTMLの .mp3.csv を取り除いたタイトル名
		html_title_name_mp3csv=html_title_name.replace(".mp3.csv","")

		# print('------------------------------')
		# ()の内容を取得
		pare_and_num=pare_com.search(html_title_name_csv).group()
		# print(pare_and_num)
		# ()の内容も含めて削除
		html_title_name_csv=pare_com.sub('',html_title_name_csv)
		html_title_name_mp3csv=pare_com.sub('',html_title_name_mp3csv)
		# print(html_title_name_csv)
		# print(html_title_name_mp3csv)

		# html_title_name_csv=html_title_name_csv.replace("_",".")
		# html_title_name_mp3csv=html_title_name_mp3csv.replace("_",".")

		# 全てに一致しなかったカウンタ
		no_find_c=True
		for (track_file_name,
				 track_title_name_sub,
				 track_title_name_mp3_sub,
				 track_title_name_space_sub) in zip(track_file_name_list,
																						track_title_name_sub_list,
																						track_title_name_mp3_sub_list,
																						track_title_name_space_sub_list):

			if track_title_name_sub==html_title_name_csv or \
				track_title_name_sub==html_title_name_mp3csv:
				if pare_and_num in track_file_name:
					file_name_str.offset(count1+1,1).value='47文字'
					no_find_c=False
			elif track_title_name_mp3_sub==html_title_name_csv or \
				track_title_name_mp3_sub==html_title_name_mp3csv:
				if pare_and_num in track_file_name:
					file_name_str.offset(count1+1,1).value='.mp3削除→47文字'
					no_find_c=False
			elif track_title_name_space_sub==html_title_name_csv.translate(tr_table) or \
				track_title_name_space_sub==html_title_name_mp3csv.translate(tr_table):
				if pare_and_num in track_file_name:
					file_name_str.offset(count1+1,1).value='スぺ削除→47文字'
					no_find_c=False
			if no_find_c==False:
				file_name_str.offset(count1+1,0).value=track_file_name
				# print(track_file_name)
				break
		if no_find_c:
			file_name_str.offset(count1+1,0).value='一致無し'
# tame11()


"""
Excelを元にしてプレイリストフォルダに音楽ファイルをコピーする

クラッシュしたので、コピー先に該当のファイルが無ければコピーする処理を追加する
"""
def tame12():
	sht_1=wb.sheets['1_一致したのだけ抽出']

	if sht_1.range(2,5).value==None:
		copy_str=sht_1.range(1,5)
	else:
		copy_str=sht_1.range(1,5).end("down")

	# プレイリスト名をリストで取得
	play_name_list=copy_str.offset(1,-4).expand("down").value
	# ファイル名をリストで取得
	track_file_name_list=copy_str.offset(1,-2).expand("down").value
	# ファイル名数を取得
	track_file_name_list_len=len(track_file_name_list)

	for count1,(play_name,track_file_name) in enumerate(zip(play_name_list,track_file_name_list)):
		print((f'-------------- {count1+1}/{track_file_name_list_len} ----------------'))
		print(play_name)
		print(track_file_name)
		move_to=play_dir+play_name
		move_file=track_dir+track_file_name
		move_file_dir=play_dir+play_name+'/'+track_file_name
		if os.path.isfile(move_file_dir):
			print('ファイルが既にあるのでパス')
			copy_str.offset(count1+1,0).value='OK'
			copy_str.offset(count1+1,1).value='OK'
		else:
			print('ファイルが無いのでコピー')
			shutil.copy(move_file,move_to)
			copy_str.offset(count1+1,0).value='OK'
			copy_str.offset(count1+1,1).value='NG'
			time.sleep(2)
		if (count1+1)%20==0:
			print('20回ごとにメモリクリア')
			# subprocess.Popen(r"C:\Users\YUTANAO\Documents\プログラム\メモリ開放.bat", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			subprocess.Popen(r"C:\Users\YUTANAO\Documents\プログラム\メモリ開放.bat").wait()
tame12()


