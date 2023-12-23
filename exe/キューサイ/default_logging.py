# ------------------------------
# ライブラリ
# ------------------------------
import logging


# ------------------------------
# logger
# ------------------------------
class Default_Logging():
	def main(self,DEBUG,log_file_name,str_format_ptn,file_format_ptn):
		logger=logging.getLogger(__name__)
		if DEBUG:
			logger.setLevel(logging.DEBUG)
			str_handler=logging.StreamHandler()
			str_handler.setLevel(logging.DEBUG)
			str_format=logging.Formatter(str_format_ptn)
			str_handler.setFormatter(str_format)
			logger.addHandler(str_handler)
		else:
			logger.setLevel(logging.DEBUG)
			str_handler=logging.StreamHandler()
			str_handler.setLevel(logging.INFO)
			str_format=logging.Formatter(str_format_ptn)
			str_handler.setFormatter(str_format)
			logger.addHandler(str_handler)
			file_handler=logging.FileHandler(log_file_name+'.log')
			file_handler.setLevel(logging.DEBUG)
			file_format=logging.Formatter(file_format_ptn)
			file_handler.setFormatter(file_format)
			logger.addHandler(file_handler)
		# 区切りをあらかじめ付加しておく
		logger.debug('------------------------------------------------------------')
		return logger