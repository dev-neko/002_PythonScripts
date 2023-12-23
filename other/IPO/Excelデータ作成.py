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


# 擬似exe化では自作関数が使えないようなのでここに関数追加した
"""------------------------------
https://qiita.com/hid_tanabe/items/3c5e6e85c6c65f7b38be
ここを参考にした

8桁文字列形式の日付(DATE = "yyyymmdd")から
平日→False、土日祝→True
を返す関数

IPOの日付は2020/07/01とか「/」入っているので置き換える処理追加した
------------------------------"""
def isHoliDay(DATE):
	DATE = DATE.replace("/", "")
	date_time = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
	if date_time.weekday() >= 5 or jpholiday.is_holiday(date_time):
		return True
	else:
		return False
"""------------------------------
https://maywork.net/computer/python-yahoo-send-mail/
ここを参考にした

Yahooからメールを送信する関数
send_mail("件名","本文")
で送信できる
------------------------------"""
def send_mail(subject,message):
	# ログイン情報、送信先設定
	from_addr="m8eV3MOvx5JJrBs@yahoo.co.jp"
	to_addr="yutaka_yutakann@yahoo.co.jp"
	passwd="X|fUYZ#b[4"
	# メールの内容設定
	msg=MIMEText(message)
	msg['Subject']=subject
	msg['From']=from_addr
	msg['To']=to_addr
	# yahooメールに接続して送信
	smtp=smtplib.SMTP("smtp.mail.yahoo.co.jp",587)
	smtp.login(from_addr,passwd)
	smtp.sendmail(from_addr,to_addr,msg.as_string())
	smtp.quit()
"""------------------------------
https://note.nkmk.me/python-datetime-day-locale-function/
ここを参考にした

bb_end = "2020/09/20"
この形式で入力すると
print(get_day_of_week_jp(bb_end))
(日)
と出力される
------------------------------"""
def get_day_of_week_jp(DATE):
	w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
	return w_list[datetime.datetime.strptime(DATE, '%Y/%m/%d').weekday()]



excel_data = ""
mail_data =[]

# URLからソースを取得
ipo_url = "http://www.tokyoipo.com/ipo/schedule.php"
get_url_parser = requests.get(ipo_url)
get_url_parser.encoding = 'EUC-JP'
bs4obj = bs4.BeautifulSoup(get_url_parser.text,'html.parser')
# print(bs4obj)

# 銘柄ごとの詳細URL取得
# ここで銘柄の詳細URLとBB開始日を取得して、BB開始日が早い順に並び替えてその順番で銘柄の詳細取得する
preurl_bbstr = []
bb_count = 0
for detail_url in bs4obj.find_all("h2",attrs={'class':'h2_ipolist_name'}):
	detail_url = detail_url.find("a").get('href')
	# preとpostで別れているので、preの場合だけその銘柄の詳細ページのソース取得
	if "pre" in detail_url:
		# 一覧ページからBB開始日取得
		bbstr = bs4obj.find_all("td",attrs={'class':'iposhcedulelist_border_all alignright'})[bb_count].text[0:5]
		bb_count+=2
		preurl_bbstr.append([detail_url,bbstr])
# BB開始日で昇順で並び替え
# preurl_bbstr.sort(reverse=True,key=lambda x: x[1]) で降順
preurl_bbstr.sort(key=lambda x:x[1])

# BB開始日が早い順に並び替えられた順番で銘柄詳細情報を取得
for preurl in preurl_bbstr:
	detail_url_parser=requests.get("http://www.tokyoipo.com"+preurl[0])
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
	# 価格か日付で分岐して整形
	# 円が入っていれば価格として,と円を消す
	if "円" in kakaku:
		kakaku=kakaku.replace(",","")
		kakaku=kakaku.replace("円","")
	# そうでなければ日付2020/01/01形式なので0埋め消す
	else:
		kakaku=datetime.datetime.strptime(kakaku,'%Y/%m/%d').strftime('%m/%d').lstrip("0").replace("/0","/")
	# ブックビルディング(開始) 取得
	bb_str = bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[16].text
	# ブックビルディング(終了) 取得
	bb_end = bs4obj_detail_url.find_all("td",attrs={'class':'main_data'})[17].text

	# 幹事団取得
	# "\xa0"が含まれていたら主幹事と判断して除外する
	kanji_list = []
	for fo_kanji in bs4obj_detail_url.find_all("td",attrs={'class':'main_data'}):
		kanji_text = fo_kanji.text
		# <td class="main_data"> でしか抽出できないので証券か證券が入っていてれば幹事団と判断
		# "\xa0"が入っている場合は主幹事なので除外
		if (("証券" in kanji_text) or ("證券" in kanji_text)) and ("\xa0" not in kanji_text):
			if "" != kanji_text:
				kanji_text = kanji_text.replace("証券","")
				kanji_text = kanji_text.replace("證券","")
				if "ＳＭＢＣ日興" == kanji_text:
					kanji_list.append("ユSM")
					kanji_list.append("ナSM")
				elif "三菱ＵＦＪモルガン・スタンレー" == kanji_text:
					kanji_list.append("ユモル")
					kanji_list.append("ナモル")
				elif "エイチ・エス"  == kanji_text:
					kanji_list.append("ユHS")
					kanji_list.append("ナHS")
				# 先頭2文字だけ抽出
				elif kanji_text in "いちよし、マネックス、みずほ、岩井コスモ、東海東京、藍澤、むさし、野村、大和、":
					kanji_list.append("ユ"+kanji_text[0:2])
					kanji_list.append("ナ"+kanji_text[0:2])
				# 応募できないところや、誤検出される語句は除外
				# webアプリに表示しないものは除外一覧で表示しないと知らないうちに野村とか除外されてるかも
				elif kanji_text in ["エース","極東","西日本シティTT","あかつき","水戸","ゴールドマン・サックスJ.Ｐ.モルガン","クレディ・スイス","豊証券","今村","ドレスナークラインオートベンソン証券会社入社","西村","BofA","UBS","静銀ティーエム","香川","特定有価信託受託者  野村信託銀行(株)","(株)大和グループ本社","・商品先物業","(株)SBI","FFG","モルガン・スタンレーMUFG","モルガン・スタンレーMUFG(株)　投資銀行本部　入社"]:
					print(f'除外:{kanji_text}')
				# 条件外の場合はそのまま結合→これなら知らない証券会社が分かる
				else:
					kanji_list.append("ユ"+kanji_text)
					kanji_list.append("ナ"+kanji_text)

	# Excelでコピペしやすいように整理

	"""
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
	"""

	# BB終了日から抽選日が平日になる日付を求める
	# +1日だと結果出てない場合が多いので+2にした
	# SBIとかは翌日発表なのでやっぱり+1にした
	bb_end_rep=bb_end.replace("/","")
	bb_end_p2=datetime.date(int(bb_end_rep[0:4]),int(bb_end_rep[4:6]),int(bb_end_rep[6:8]))+datetime.timedelta(days=1)
	while True:
		if isHoliDay(bb_end_p2.strftime('%Y%m%d')):
			bb_end_p2=bb_end_p2+datetime.timedelta(days=1)
		else:
			bb_kekka = bb_end_p2.strftime('%Y/%m/%d')
			break

	# Excelでコピペしやすいようにタブ付加して結合
	# 0埋めを削除
	excel_data = excel_data + ipo_name+"\t"+\
							 datetime.datetime.strptime(bb_str,'%Y/%m/%d').strftime('%m/%d').lstrip("0").replace("/0","/")+get_day_of_week_jp(bb_str)+"\t"+\
							 datetime.datetime.strptime(bb_end,'%Y/%m/%d').strftime('%m/%d').lstrip("0").replace("/0","/")+get_day_of_week_jp(bb_end)+"\t"+\
							 datetime.datetime.strptime(bb_kekka,'%Y/%m/%d').strftime('%m/%d').lstrip("0").replace("/0","/")+get_day_of_week_jp(bb_kekka)+"\t"+\
							 kakaku

	# 幹事団まとめ
	for count, fo_kanji_list in enumerate(kanji_list):
		# 13で割り切れれば、改行文字+タブ文字5個にする、0を割ると余り0になるので+1した
		if (count+1) % 13 == 0:
			excel_data = excel_data + "\n\t\t\t\t\t" + fo_kanji_list
		else:
			excel_data = excel_data +"\t"+ fo_kanji_list
	excel_data = excel_data + "\n"


# 結果出力
pyperclip.copy(excel_data)
# send_mail("IPOデータ",excel_data)