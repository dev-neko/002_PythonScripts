import bs4
import requests
import re


# URLからソースを取得
src_url = "https://auctions.yahoo.co.jp/search/search?p=python3&va=python3&b=1&n=20&mode=2"
# src_url="https://auctions.yahoo.co.jp/category/list/2084024206/?p=%E3%83%A2%E3%83%8E%E3%82%B0%E3%83%A9%E3%83%A0%E3%83%A9%E3%82%A4%E3%83%B3&auccat=2084024206&exflg=1&b=1&n=20&s1=score2&o1=d&mode=2&brand_id=102176&nockie=1&auchours=1"
src_url_parser = requests.get(src_url)
bs4obj = bs4.BeautifulSoup(src_url_parser.text,'html.parser')
# print(bs4obj)

# 検索結果一覧ページから取得できる情報を取得
for list_items in bs4obj.find_all("h3",attrs={'class':'Product__title'}):
	# オークション名
	auc_title = list_items.find("a",attrs={'class':'Product__titleLink'}).text
	# URL
	auc_url = list_items.find("a",attrs={'class':'Product__titleLink'}).get('href')

	# URLからソースを取得
	src_url=auc_url
	# src_url="https://page.auctions.yahoo.co.jp/jp/auction/m448053370"
	src_url_parser=requests.get(src_url)
	bs4obj2=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	# 自動延長の有無
	auc_auto_ext=bs4obj2.find("ul",attrs={'class':'ProductDetail__items ProductDetail__items--primary'}).find_all("dd",attrs={'class':'ProductDetail__description'})[
		3].text
	# print(auc_url)
	# print(auc_auto_ext)

for list_items in bs4obj.find_all("a",attrs={'class':'Product__seller'}):
	# 出品者名
	auc_seller = list_items.text
for list_items in bs4obj.find_all("a",attrs={'class':'Product__rating'}):
	# 出品者のレート
	auc_rating = list_items.text
for list_items in bs4obj.find_all("div",attrs={'class':'Product__priceInfo'}):
	# 現在価格
	auc_price=list_items.find("span",attrs={'class':'Product__priceValue u-textRed'}).text
	# 即決価格
	if list_items.select('span[class="Product__priceValue"]'):
		auc_pricewin=list_items.select('span[class="Product__priceValue"]')[0].text
	else:
		auc_pricewin="即決価格無し"
for list_items in bs4obj.find_all("div",attrs={'class':'Product__otherInfo cf'}):
	# 入札数
	auc_bid=list_items.find("a",attrs={'class':'Product__bid'}).text
	# 残り日数か時間か分
	auc_time_dayhormin=list_items.find("span",attrs={'class':'Product__time'}).text
	# 終了日時
	auc_time_detail=list_items.find("span",attrs={'class':'u-textGray u-fontSize10'})
	# 残り時間は「残り日数か時間」と「終了日時」か「残り分」だけの組み合わせなので
	# 「終了日時」があれば「残り日数か時間」と「終了日時」を表示
	# 「終了日時」がなければ「残り分」だけ表示
	if auc_time_detail:
		auc_time=auc_time_dayhormin+auc_time_detail.text
	else:
		auc_time=auc_time_dayhormin
for list_items in bs4obj.find_all("img",attrs={'class':'Product__imageData'}):
	# 画像URL
	auc_imgurl=list_items.get('src')

# 現在価格と即決価格が同じならば定額、異なればオークション



# break

