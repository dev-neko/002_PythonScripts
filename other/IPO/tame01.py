# coding: utf8

# Yahooからメールを送信するサンプル


import smtplib
from email.mime.text import MIMEText


def send_mail(subject,message):
	# ログイン情報、送信先設定
	from_addr="m8eV3MOvx5JJrBs@yahoo.co.jp"
	to_addr="yutaka_yutakann@yahoo.co.jp"
	passwd="X|fUYZ#b[4"
	# メールの内容設定
	msg=MIMEText(message)
	msg['Subject']=subject
	msg['From']=from_addr
	msg['To']=to_addr
	# yahooメールに接続して送信
	smtp=smtplib.SMTP("smtp.mail.yahoo.co.jp",587)
	smtp.login(from_addr,passwd)
	smtp.sendmail(from_addr,to_addr,msg.as_string())
	smtp.quit()

send_mail("Pythonメール送信","ぼへぇ")