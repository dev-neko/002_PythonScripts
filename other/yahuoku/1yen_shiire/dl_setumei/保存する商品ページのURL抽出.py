"""
使い方
落札分一覧のソース.txt に抽出したいURLがあるソースを貼り付ける
実行する
urllist.txt に抽出したURLが記載される
前のURLは消されるので注意
"""
"""
2020年7月3日
	本来なら重複するURLを検出したり、すべてのページで抽出できるようにしたり
	前のURL消さないようにしたいけど、とりあえず出来たのでそれは次回にした
"""


import re


with open('落札分一覧のソース.txt') as f:
	lines = f.read()
	# https://page.auctions.yahoo.co.jp/jp/auction/ で始まって " で終わる間の文字列が欲しい
	# () で囲った中身が取り出される
	# 前後にも文字列があるので、それを考慮するとこうなるらしい
	aa = re.findall(r'.*(https://page.auctions.yahoo.co.jp/jp/auction/.*?)".*', lines)

with open('urllist.txt',mode='w') as f:
	# リストを要素ごとに改行させて書き込むにはこうするらしい
	f.write('\n'.join(aa))