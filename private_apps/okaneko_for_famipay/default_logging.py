# ------------------------------
# ライブラリ
# ------------------------------
import logging


# ------------------------------
# logger
# ------------------------------
class Default_Logging():
	def __init__(self):
		self.str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
		self.file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'

	def main(self,DEBUG,log_file_name):
		logger=logging.getLogger(__name__)
		if DEBUG:
			logger.setLevel(logging.DEBUG)
			str_handler=logging.StreamHandler()
			str_handler.setLevel(logging.DEBUG)
			str_format=logging.Formatter(self.str_format_ptn)
			str_handler.setFormatter(str_format)
			logger.addHandler(str_handler)
		else:
			logger.setLevel(logging.DEBUG)
			str_handler=logging.StreamHandler()
			str_handler.setLevel(logging.INFO)
			str_format=logging.Formatter(self.str_format_ptn)
			str_handler.setFormatter(str_format)
			logger.addHandler(str_handler)
			file_handler=logging.FileHandler(log_file_name+'.log')
			file_handler.setLevel(logging.DEBUG)
			file_format=logging.Formatter(self.file_format_ptn)
			file_handler.setFormatter(file_format)
			logger.addHandler(file_handler)
		# 区切りをあらかじめ付加しておく
		logger.debug('------------------------------------------------------------')
		return logger