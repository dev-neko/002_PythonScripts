import random
import re
import secrets
import string


class Ac_Data_Class():
	def __init__(self,args):
		self.args=args

	# プロフィールデータを作成
	def cre_data(self,cre_mailaddr):
		# 性別
		sex_list=['男性','女性']
		rand_sex=random.choice(sex_list)
		# 生年月日
		rand_year="19"+str(random.randrange(60,92))
		rand_month=str(random.randint(1,12))
		rand_birth=rand_month+'/'+rand_year
		# 職業
		employ_list=['会社員(正社員)','会社員(契約/派遣)','会社役員','公務員','専門家(医師・弁護士・会計士など)','自営業','自由業(フリーランス)','パート・アルバイト','大学生・短大生・大学院生・その他学生','専業主婦','無職','その他']
		rand_employ=random.choice(employ_list)
		# QPW
		size=12
		chars=string.ascii_uppercase+string.ascii_lowercase+string.digits
		rand_pw=''.join(secrets.choice(chars) for x in range(size))
		# 苗字
		prof_lname=self.args.sht_name_jp.range(1,1).expand('down').value
		rand_lname=prof_lname[random.randint(0,len(prof_lname)-1)]
		# 名前
		if rand_sex=='男性':
			prof_fname=self.args.sht_name_jp.range(1,2).expand('down').value
			rand_fname=prof_fname[random.randint(0,len(prof_fname)-1)]
		elif rand_sex=='女性':
			prof_fname=self.args.sht_name_jp.range(1,3).expand('down').value
			rand_fname=prof_fname[random.randint(0,len(prof_fname)-1)]
		# ユーザー名
		regex=re.search(r'(.*)(?=@)',cre_mailaddr)
		# 5文字以内になることがあるので5文字の数字とアルファベット小文字を足す
		size=5
		chars=string.ascii_lowercase+string.digits
		rand_username=regex.group()+''.join(secrets.choice(chars) for x in range(size))

		ac_data_list=[
			cre_mailaddr,
			rand_username,
			rand_pw,
			rand_birth,
			rand_sex,
			rand_employ,
			rand_lname,
			rand_fname,
		]
		ac_data_dict={
			'メールアドレス':cre_mailaddr,
			'ユーザー名':rand_username,
			'QPW':rand_pw,
			'生年月日':rand_birth,
			'性別':rand_sex,
			'職業':rand_employ,
			'苗字':rand_lname,
			'名前':rand_fname
		}

		return ac_data_list,ac_data_dict