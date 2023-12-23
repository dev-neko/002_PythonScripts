import bs4
import requests
import re


# URLからソースを取得
src_url = "https://auctions.yahoo.co.jp/search/advanced?p=%E3%81%82&va=%E3%81%82&exflg=1&b=1&n=20&mode=2&f=0x2"
# src_url="https://auctions.yahoo.co.jp/category/list/2084024197/?p=%E3%81%8B%E3%81%B0%E3%82%93%E3%80%81%E3%83%90%E3%83%83%E3%82%B0&auccat=2084024197&exflg=1&b=1&n=100&s1=end&o1=a&mode=2&brand_id=102176&nockie=1"
src_url_parser = requests.get(src_url)
bs4obj = bs4.BeautifulSoup(src_url_parser.text,'html.parser')
# print(bs4obj)

for count, list_items in enumerate(bs4obj.find_all("label",attrs={'for':re.compile('^loc_cd')})):
	print(list_items.text.replace(" ","").replace("\n","")+":"+"%2C"+str(count))

# for list_items in bs4obj.find_all("label",attrs={'for':re.compile('^other_cat')}):
# 	print('"'+list_items.text.replace(" ","").replace("\n","")+'"'+":"+'"'+str(list_items.find("input",attrs={'type':'radio'}).get('value'))+'",')

