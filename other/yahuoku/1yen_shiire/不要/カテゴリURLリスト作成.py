from jinja2 import Template
import requests, bs4


# ------------------------------
# URL作成 ここから

cate_url_1 = "https://auctions.yahoo.co.jp/category/list/"
cate_url_2 = "&fixed=2&aucmaxprice=1&price_type=currentprice&max=1&pstagefree=1&exflg=1&b=1&n=100&s1=bids&o1=d&auchours="
# オークションの残り時間
auchours = "48"
# 除外出品者ID
# exsid = "&exsid=y_b_r_2010%2Cixdcu81410%2Cvenrx80915"
exsid = ""

cate_no = []
cate_name = []
cate_url = []
jinja_data = []

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
	cate_url.append(cate_url_1 + cate_no[n] + "/?p=" + cate_name[n] + "&auccat=" + cate_no[n] + cate_url_2 + auchours + exsid)
	# print(cate_url)
	# print(cate_url[n])

# jinjaのdata作成
for cate_name,cate_url in zip(cate_name,cate_url):
	jinja_data.append({'cate_name':cate_name, 'cate_url':cate_url})

# URL作成 ここまで
# ------------------------------
# URLにアクセスして情報取得 ここから

# 48時間以内でも100件以内なので2ページ目は考慮しない、と思ったけど100件以上ありそうだから考慮する
# 「アクセサリー、時計」

# 入札無し
# 除外キーワード→相互評価、


# URLにアクセスして情報取得 ここまで
# ------------------------------
# jinjaでHTML作成 ここから

# HTMLテンプレート
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
	<ol>
	{% for item in navigation %}
		<li><a href="{{ item.cate_url }}" target = "_blank">{{ item.cate_name}}</a></li>
	{% endfor %}
	</ol>
</body>
</html>
'''

#テンプレートへの挿入
template = Template(html)
data = {'navigation' :jinja_data}
genhtml = template.render(data)

#ファイルへの書き込み
genfile = open("URLリスト.html",'w') #書き込みモードで開く
genfile.write(genhtml)
genfile.close()

# jinjaでHTML作成 ここまで
# ------------------------------