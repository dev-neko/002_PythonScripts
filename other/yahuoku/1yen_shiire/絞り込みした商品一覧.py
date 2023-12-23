from jinja2 import Environment, FileSystemLoader
import requests, bs4
import datetime


# ------------------------------
# ------------------------------
# 変数 ここから

# ------------------------------

# オークションの残り時間

# auchours = "24"
# auchours = "36"
auchours = "48"

# ------------------------------

# 除外するキーワード 「、」で区切る

# 必要な商品も除外されてしまうので一旦使用止める
# exc_word = "相互評価、画像、そうご評価、紹介、招待、引き取り、副業、一人一枚、" \
# 					 "直接引取り、バイナリー、ツール、アフィリエイト、登録、稼ぐ、稼げる、" \
# 					 "稼ぎ、収入、方法、即金、不労所得、打ち出の小槌、ＦＸ、FX、"
# 、を|に変換
# exc_word = exc_word.replace('、', '|')

# ------------------------------

# 除外する出品者ID 「、」で区切る

"""
aoto_station、takasago_station
	落札できないキックスクーターしか出品していない
jeeponoff
	無料ポケットWi-Fiの出品しかしていない
y_b_r_2010、ixdcu81410、takakusagi3751、vwgfc32234、fxc5a1958、tutinoko1290
	相互評価の画像がほとんどで、その他も1円の出品はしていないし、まともな人じゃなさそう
	たまに普通の商品出品しているのでその点はどうにかしたい
cold_black_1978、starcats_0922、fysfc848、nhe2016、syoma07245、mergus_albellus_1115、wsbfl24414、hyyib79076、xr_honey08
	その他カテゴリの胡散臭い商材だけ
"""
exc_seller = "aoto_station、takasago_station、jeeponoff、y_b_r_2010、ixdcu81410、vwgfc32234、fxc5a1958、tutinoko1290、cold_black_1978、fysfc848、hyyib79076、xr_honey08"

# 除外出品者のオークション一覧ページのURLをjinja形式でまとめる
# 現在1円、送料無料 の条件を付加
jinja_data_exc=[]
exc_seller_list = exc_seller.split('、')
for fo_exc_seller_list in exc_seller_list:
	exc_url = "https://auctions.yahoo.co.jp/seller/" + fo_exc_seller_list + "?sid=" + fo_exc_seller_list + "&aucmaxprice=1&price_type=currentprice&max=1&pstagefree=1&b=1&n=100&s1=bids&o1=d&slider=undefined"
	jinja_data_exc.append({'exc_seller':fo_exc_seller_list,'exc_url':exc_url,})

# 、を%2Cに変換してURLに対応
exc_seller = "&exsid=" + exc_seller.replace('、', '%2C')

# 変数 ここまで
# ------------------------------
# ------------------------------
# 検索条件などをjinja形式でまとめる ここから

"""
取得時間、終了時間、
"""

# 取得時間取得
dt_now = f'{datetime.datetime.now():%Y/%m/%d %H:%M:%S}'

jinja_data_other = {'gettime':dt_now,'limit':auchours}

# 検索条件などをjinja形式でまとめる ここまで
# ------------------------------
# URL作成 ここから

# 絞り込み内容
# 現在 ～1円、送料無料、オークション、？時間以内
cate_url_1 = "https://auctions.yahoo.co.jp/category/list/"
cate_url_2 = "&fixed=2&aucmaxprice=1&price_type=currentprice&max=1&pstagefree=1&exflg=1&b=1&n=100&s1=bids&o1=d&auchours="

cate_no = []
cate_name = []
cate_url = []
jinja_data = []
jinja_data_cate = []

f = open('category.txt')
lines = f.readlines()

# カテゴリー番号抽出
for fa in lines[::2]:
	# print(fa.strip())
	cate_no.append(fa.strip())

# カテゴリー名抽出
for fa in lines[1::2]:
	# print(fa.strip())
	cate_name.append(fa.strip())

# URL作成
for n,fa in enumerate(cate_no):
	cate_url.append(cate_url_1 + cate_no[n] + "/?p=" + cate_name[n]
									+ "&auccat=" + cate_no[n] + cate_url_2 + auchours + exc_seller)
# print(cate_url[n])

# URL作成 ここまで
# ------------------------------
# URLにアクセスして情報取得 ここから

"""
48時間以内でも100件以内なので2ページ目は考慮しない？
と思ったけど100件以上ありそうだから考慮する？

アダルトカテゴリはログインしないと表示されない
→もともと不要なのでOK
"""

# コンピューターカテゴリだけで試す場合に使用
cate_name = []
cate_url = []
cate_name.append("aheahe")
cate_url.append("https://auctions.yahoo.co.jp/category/list/23336/?p=コンピュータ&auccat=23336&fixed=2&aucmaxprice=1&price_type=currentprice&max=1&pstagefree=1&exflg=1&b=1&n=100&s1=bids&o1=d&auchours=48&exsid=aoto_station%2Ctakasago_station%2Cjeeponoff")

# 取得したURLの分だけループ
for (fo_cate_name,fo_cate_url) in zip(cate_name,cate_url):

	print(fo_cate_name + " 取得中")
	get_url_info = requests.get(fo_cate_url)
	bs4obj = bs4.BeautifulSoup(get_url_info.text, 'html.parser')
	# print(bs4obj)
	# オークションの出品数を取得
	itemnum_parser = bs4obj.find("li", class_="Tab__item Tab__item--current" )
	itemnum_parser = itemnum_parser.find(class_="Tab__subText" ).text
	# 件数を数字に変換
	itemnum_parser = int(itemnum_parser.replace( "件", "" ))
	# カテゴリー名、URL、総件数 をjinja形式まとめる
	jinja_data_cate.append({'cate_name':fo_cate_name,'cate_url':fo_cate_url,
													'itemnum':itemnum_parser,})

	# オークションのソース取得、定額のソースは無視
	getsource = bs4obj.find("div", class_="Products__list")
	# find_all で見つからない(出品0件)と例外発生するのでtryでキャッチして、その場合は何もしない
	try:
		# 画像のURL取得
		imgurl_parser = getsource.find_all("img", class_="Product__imageData" )
		# 商品ページのURL取得
		# titleもURLも同じタグに入っているので、そのあとの['href']['title']で内容を取得している
		prourl_parser = getsource.find_all(class_="Product__titleLink" )
		# 商品タイトル取得
		protit_parser = getsource.find_all(class_="Product__titleLink" )
		# 入札数取得
		bidnum_parser = getsource.find_all(class_="Product__bid" )
		# 残り時間取得
		limtime_parser = getsource.find_all(class_="Product__time" )
		# jinjaに送るデータ形式でまとめる
		for (fo_imgurl_parser,fo_prourl_parser,fo_protit_parser,fo_bidnum_parser,fo_limtime_parser
				 ) in zip(imgurl_parser,prourl_parser,protit_parser,bidnum_parser,limtime_parser):
			# 入札が0なら追加
			if fo_bidnum_parser.string == "0":
			# キーワードで除外するパターン
			# if (fo_bidnum_parser.string=="0" and
			# 	re.search(exc_word,fo_protit_parser['title'])==None
			# ):
				jinja_data.append({'imgurl':fo_imgurl_parser['src'],
													 'prourl':fo_prourl_parser['href'],
													 'protit':fo_protit_parser['title'],
													 'bidnum':fo_bidnum_parser.string,
													 'limtime':fo_limtime_parser.string,
													 })
	except AttributeError:
		# print("出品無し")
		pass

# URLにアクセスして情報取得 ここまで
# ------------------------------
# jinjaでHTML作成 ここから

#テンプレートへ挿入
data = {'jinja_data':jinja_data,
				'jinja_data_cate':jinja_data_cate,
				'other':jinja_data_other,
				'exc':jinja_data_exc,
				}

print(data)

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('jinja_template.html')
genhtml = template.render(data)

#ファイルへの書き込み
genfile = open("まとめ.html",'w') #書き込みモードで開く
genfile.write(genhtml)
genfile.close()

# jinjaでHTML作成 ここまで
# ------------------------------
