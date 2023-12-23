import re
import sys

hope_day_time_list=['', '', 'ご希望日を選択してください', '', '', '6月6日', '', '××××××××', '6月7日', '××××××××', '6月8日', '×××1××××', '6月9日', '××××××××', '6月10日', '××××××××', '6月11日', '××××××××', '', '6月12日', '', '××××××××', '']

res_day='6月8日'

free_border=hope_day_time_list[hope_day_time_list.index(res_day)+1]
if free_border=="":
	free_border=hope_day_time_list[hope_day_time_list.index(res_day)+2]
print(f'ページ内の空き枠情報\n{hope_day_time_list}')
print(f'予約希望日の空き枠情報：{res_day}{free_border}')
if bool(re.search(r'\d',free_border)):
	print('予約希望日の枠が空いているため、8時30分まで待機します。')
else:
	print('予約手続き前に既に枠が埋まっているため終了します。')
	sys.exit()