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
import locale


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



bb_end = "2020/09/20"

def get_day_of_week_jp(DATE):
	w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
	return w_list[datetime.datetime.strptime(DATE, '%Y/%m/%d').weekday()]

print(get_day_of_week_jp(bb_end))

