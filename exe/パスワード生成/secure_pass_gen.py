"""------------------------------
記録

secretsは暗号学的に強い乱数を作成できるらしい
推奨は英数12文字以上

確実に4種類の文字を入れるパスワードの作成方法
4種から順番に取り出す
その後は希望文字数になるまで4種からランダムに取り出す
希望文字数内で順番をランダムにする

やる事
記号と数字が含まれていることを確認して足りない場合は再作成する
候補をいくつか同時に表示してコピーできる
------------------------------"""

# ------------------------------
# ライブラリ
# ------------------------------
import random
import secrets
import string

# ------------------------------
# 定数
# ------------------------------


# ------------------------------
# 関数・クラス
# ------------------------------
def pass_gen(size,symbol_sw):
	"""
	:param size: パスワードの文字数
	:param symbol_sw: 記号を含む場合はON
	:return: 生成したパスワード
	"""

	# string.ascii_uppercase  アルファベット大文字
	# string.ascii_lowercase  アルファベット小文字
	# string.digits           数字
	# string.punctuation      記号

	# 使用する文字列を記号以外で設定
	# 記号以外の3種類を1回ずつ使用してパスワード生成
	chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
	cre_pass=''
	cre_pass += ''.join(secrets.choice(string.ascii_uppercase))
	cre_pass += ''.join(secrets.choice(string.ascii_lowercase))
	cre_pass += ''.join(secrets.choice(string.digits))
	# print(chars,cre_pass)

	# 記号SWがONの場合は、使用する文字列に記号を追加、記号を1回使用してパスワード生成
	if symbol_sw=='ON':
		chars += string.punctuation
		cre_pass += ''.join(secrets.choice(string.punctuation))
		# print(chars,cre_pass)

	# 指定した文字数以内の場合は使用する文字列から選んでパスワード生成
	while len(cre_pass)<size:
		cre_pass += ''.join(secrets.choice(chars))
		# print(cre_pass)

	# 生成したパスワードをランダムに並び替える
	sort_cre_pass = ''.join(random.sample(cre_pass, len(cre_pass)))
	# print(sort_cre_pass)

	return sort_cre_pass

# ------------------------------
# main
# ------------------------------
# pass_gen(12,'ON')
# print(pass_gen(3,symbol))