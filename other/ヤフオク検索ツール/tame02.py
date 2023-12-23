import bs4
import requests
import re


# URLからソースを取得
src_url = "https://auctions.yahoo.co.jp/search/search?p=python3&va=python3&b=1&n=20&mode=2"
src_url="https://auctions.yahoo.co.jp/search/search?&va=bbb&vo=&ve=&ngram=0&abatch=0&fixed=3&auccat=0&aucminprice=&aucmaxprice=&aucmin_bidorbuy_price=&aucmax_bidorbuy_price=&istatus=&loc_cd=0&mode=2&n=20"
src_url_parser = requests.get(src_url)
bs4obj = bs4.BeautifulSoup(src_url_parser.text,'html.parser')
# print(bs4obj)
# 検索結果一覧ページから取得できる情報を取得
for list_items in bs4obj.find_all("li",attrs={'class':'Product'}):
	# 画像URL
	auc_imgurl=list_items.find("img",attrs={'class':'Product__imageData'}).get('src')
	# オークション名
	auc_title = list_items.find("a",attrs={'class':'Product__titleLink'}).text
	# URL
	auc_url = list_items.find("a",attrs={'class':'Product__titleLink'}).get('href')
	# 出品者名
	auc_seller = list_items.find("a",attrs={'class':'Product__seller'}).text
	# 出品者のレート
	# 新規はレート無しなのでそれを考慮
	auc_rating=list_items.find("a",attrs={'class':'Product__rating'})
	if auc_rating:
		auc_rating=auc_rating.text
	else:
		auc_rating="0%"
	# 現在価格
	auc_price=list_items.find("span",attrs={'class':'Product__priceValue u-textRed'}).text.replace(",","").replace("円","")
	# 即決価格
	if list_items.select('span[class="Product__priceValue"]'):
		auc_pricewin=list_items.select('span[class="Product__priceValue"]')[0].text.replace(",","").replace("円","")
	else:
		auc_pricewin="-"
	# 入札数
	auc_bid=list_items.find("a",attrs={'class':'Product__bid'}).text
	# 残り時間(auc_time)は「残り日数か時間」と「終了日時」か「残り分」だけの組み合わせなので
	# 「終了日時」があれば「残り日数か時間」と「終了日時」を表示
	# 「終了日時」がなければ「残り分」だけ表示
	auc_time_dayhormin=list_items.find("span",attrs={'class':'Product__time'}).text
	auc_time_detail=list_items.find("span",attrs={'class':'u-textGray u-fontSize10'})
	if auc_time_detail:
		auc_time=auc_time_dayhormin+auc_time_detail.text
	else:
		auc_time=auc_time_dayhormin
	# 現在価格と即決価格が同じならば定額、異なればオークションと判断して
	# オークションの場合だけ自動延長の有無を確認
	# URLからソースを取得
	if auc_price != auc_pricewin:
		src_url=auc_url
		src_url_parser=requests.get(src_url)
		bs4obj2=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# 自動延長の有無
		auc_auto_ext=bs4obj2.find("ul",attrs={'class':'ProductDetail__items ProductDetail__items--primary'}).find_all("dd",attrs={'class':'ProductDetail__description'})[
			3].text.replace("：","")
	else:
		auc_auto_ext="定額"

	print(auc_title)
	print(auc_auto_ext)

# break

