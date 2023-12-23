# ------------------------------
# ライブラリ
# ------------------------------
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from tqdm import tqdm
import xlwings
from bs4 import BeautifulSoup

# ------------------------------
# class
# ------------------------------
class get_add:
	def __init__(self,target_url):
		# URLからソースを取得
		self.bs4obj=BeautifulSoup(requests.get(target_url).text,'html.parser')
		pass
	def prt(self):
		print(self.bs4obj)





# ------------------------------
# main
# ------------------------------

ytv_url='https://www.youtube.com/watch?v=69BmIH61zzg'

def main():
	ga=get_add(ytv_url)
	ga.prt()
main()

