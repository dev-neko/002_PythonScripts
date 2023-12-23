"""------------------------------
secretsは暗号学的に強い乱数を作成できるらしい
推奨は英数12文字以上
記号が必要な場合は第二引数に必要な記号を記入する


やる事
記号と数字が含まれていることを確認して足りない場合は再作成する
候補をいくつか同時に表示してコピーできる
------------------------------"""


import re
import secrets
import string
import time


def pass_gen(size,symbol):
	# string.ascii_uppercase→アルファベット大文字
	# string.ascii_lowercase→アルファベット小文字
	# string.digits→数字
	# 記号一覧はここを参考にした
	# https://www.touki-kyoutaku-online.moj.go.jp/password/password_available.html


	chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation


	symbol_list='|'.join(symbol)
	print(symbol_list)

	while True:
		cre_pass = ''.join(secrets.choice(chars) for pass_size in range(size))
		print(cre_pass)
		# 記号が空ならば、数字が含まれていればbreak
		# 記号が空でなければ、数字と記号が含まれていればbreak
		print(re.search("[0-9]", cre_pass))
		print(re.search("[a-z]", cre_pass))
		print(re.search("[A-Z]", cre_pass))
		print(re.search("!|\"|#|$|%|&|'|\(|\)|\*|\+|,|-|.|/|:|;|<|=|>|\?|@|\[|\|]|^|_|`|\{|\||}|~", cre_pass))
		if (re.search("[0-9]", cre_pass)) and (re.search("!|\"|#|$|%|&|'|\(|\)|\*|\+|,|-|.|/|:|;|<|=|>|\?|@|\[|\|]|^|_|`|{|\||}|~", cre_pass)) and (re.search("[a-z]", cre_pass)) and (re.search("[A-Z]", cre_pass)):
			break
		else:
			time.sleep(0.1)
	return cre_pass

# symbol="!#$%&'()=~|`\"{+*}?_-^\@[;:],./<>"
symbol=string.punctuation
# symbol=""

pass_gen(4,symbol)
# print(pass_gen(3,symbol))


