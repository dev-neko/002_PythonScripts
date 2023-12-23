'''
pop3でメールを受信する

戻り値
受信したメルの
From ヘッダ（差出人）
Date ヘッダ（送信日時）
Subject ヘッダ（件名）
本文

使い方
from my_module import mail_receiving_pop3
をインポート

メル受信したり件数取得したいたびに実行する必要有るので変数に入れたほうが楽
pop3_serv = 'pop.mail.yahoo.co.jp'
pop3_user = 'trashmail_receive_001'
pop3_pass = 'j50fBU1PvH'
cli = poplib.POP3(pop3_serv)
cli.user(pop3_user)
cli.pass_(pop3_pass)

受信したいメルの順番は受信した順番が古いほど数字が小さくなる→1番古いのは1
from_, date, subject, content
の順でタプルで入っているので
msg = mail_receiving_pop3.fetchmail(cli, 受信したいメルの順番)[3]
print(msg)
にすると本文をプリントできる
'''

import email
from email.header import decode_header

# メールを受信する
def fetchmail(cli, msg_no):
	content = cli.retr(msg_no)[1]
	msg = email.message_from_bytes(b'\r\n'.join(content))
	# From ヘッダ（差出人）
	from_ = get_header(msg, 'From')
	# Date ヘッダ（送信日時）
	date = get_header(msg, 'Date')
	# Subject ヘッダ（件名）
	subject = get_header(msg, 'Subject')
	# 本文
	content = get_content(msg)
	return from_, date, subject, content
	# return content


# ヘッダを取得
def get_header(msg, name):
	header = ''
	if msg[name]:
		for tup in decode_header(str(msg[name])):
			if type(tup[0]) is bytes:
				charset = tup[1]
				if charset:
					header += tup[0].decode(tup[1])
				else:
					header += tup[0].decode()
			elif type(tup[0]) is str:
				header += tup[0]
	return header


# 本文を取得
def get_content(msg):
	charset = msg.get_content_charset()
	payload = msg.get_payload(decode=True)
	try:
		if payload:
			if charset:
				return payload.decode(charset)
			else:
				return payload.decode()
		else:
			return ""
	except:
		return payload # デコードできない場合は生データにフォールバック


