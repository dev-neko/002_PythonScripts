# ------------------------------
# ライブラリ
# ------------------------------
import random
import re
import secrets
import string


# ------------------------------
# 処理関数・クラス
# ------------------------------
class Ac_Data_Class():
	def __init__(self):
		# self.args=args
		pass

	# プロフィールデータを作成
	def cre_data(self):
		# ニックネーム
		size=random.randint(3,5)
		if random.choice(['ひらがな','カタカナ'])=='ひらがな':
			rand_nickname=''.join(chr(random.randint(ord('あ'),ord('ん'))) for _ in range(size))
		else:
			rand_nickname=''.join(chr(random.randint(ord('ア'),ord('ン'))) for _ in range(size))
		# PW
		while True:
			size=random.randint(8,12)
			chars=string.ascii_uppercase+string.ascii_lowercase+string.digits
			rand_pw=''.join(secrets.choice(chars) for _ in range(size))
			# 数字が含まれるまでループする
			if any(map(str.isdigit, rand_pw)): break

		# Excelに追記用
		ac_data_list=[
			rand_nickname,
			rand_pw,
		]
		# 登録時に使用
		ac_data_dict={
			'ニックネーム':rand_nickname,
			'PW':rand_pw,
		}

		return ac_data_list,ac_data_dict