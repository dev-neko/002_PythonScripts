"""
全国に対応
"""

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
# DEBUG・初期設定
# ------------------------------
# DEBUG=False
DEBUG=True

if DEBUG:
	import winsound
	heroku_login_url='http://127.0.0.1:8000/accounts/login/'
	heroku_bd_url="http://127.0.0.1:8000/dballdata/"
else:
	heroku_login_url='https://camera-shop-alert.herokuapp.com/accounts/login/'
	heroku_bd_url="https://camera-shop-alert.herokuapp.com/dballdata/"

TOKYO="https://www.kango-roo.com/career/search/results.php?mode=area&areas=3&prefs=13&allCities=1%2C2%2C3&cities=13101%2C13102%2C13103%2C13104%2C13105%2C13106%2C13107%2C13108%2C13109%2C13110%2C13111%2C13112%2C13113%2C13114%2C13115%2C13116%2C13117%2C13118%2C13119%2C13120%2C13121%2C13122%2C13123%2C13201%2C13202%2C13203%2C13204%2C13205%2C13206%2C13207%2C13208%2C13209%2C13210%2C13211%2C13212%2C13213%2C13214%2C13215%2C13218%2C13219%2C13220%2C13221%2C13222%2C13223%2C13224%2C13225%2C13227%2C13228%2C13229%2C13303%2C13305%2C13307%2C13308%2C13361%2C13362%2C13363%2C13364%2C13381%2C13382%2C13401%2C13402%2C13421&lineCats=&lines=&allStations=&stations=&selectedStationInfo=&keyword="
KANAGAWA="https://www.kango-roo.com/career/search/results.php?mode=area&areas=3&prefs=14&allCities=4%2C5%2C6%2C7%2C114&cities=14101%2C14102%2C14103%2C14104%2C14105%2C14106%2C14107%2C14108%2C14109%2C14110%2C14111%2C14112%2C14113%2C14114%2C14115%2C14116%2C14117%2C14118%2C14131%2C14132%2C14133%2C14134%2C14135%2C14136%2C14137%2C14151%2C14152%2C14153%2C14201%2C14203%2C14204%2C14205%2C14206%2C14207%2C14208%2C14210%2C14211%2C14212%2C14213%2C14214%2C14215%2C14216%2C14217%2C14218%2C14301%2C14321%2C14341%2C14342%2C14361%2C14362%2C14363%2C14364%2C14366%2C14382%2C14383%2C14384%2C14401%2C14402&lineCats=&lines=&allStations=&stations=&selectedStationInfo=&keyword="
SAITAMA="https://www.kango-roo.com/career/search/results.php?mode=area&areas=3&prefs=11&allCities=8%2C9%2C10&cities=11101%2C11102%2C11103%2C11104%2C11105%2C11106%2C11107%2C11108%2C11109%2C11110%2C11201%2C11202%2C11203%2C11206%2C11207%2C11208%2C11209%2C11210%2C11211%2C11212%2C11214%2C11215%2C11216%2C11217%2C11218%2C11219%2C11221%2C11222%2C11223%2C11224%2C11225%2C11227%2C11228%2C11229%2C11230%2C11231%2C11232%2C11233%2C11234%2C11235%2C11237%2C11238%2C11239%2C11240%2C11241%2C11242%2C11243%2C11245%2C11246%2C11301%2C11324%2C11326%2C11327%2C11341%2C11342%2C11343%2C11346%2C11347%2C11348%2C11349%2C11361%2C11362%2C11363%2C11365%2C11369%2C11381%2C11383%2C11385%2C11408%2C11442%2C11464%2C11465&lineCats=&lines=&allStations=&stations=&selectedStationInfo=&keyword="
CHIBA="https://www.kango-roo.com/career/search/results.php?mode=area&areas=3&prefs=12&allCities=11%2C12%2C13&cities=12101%2C12102%2C12103%2C12104%2C12105%2C12106%2C12202%2C12203%2C12204%2C12205%2C12206%2C12207%2C12208%2C12210%2C12211%2C12212%2C12213%2C12215%2C12216%2C12217%2C12218%2C12219%2C12220%2C12221%2C12222%2C12223%2C12224%2C12225%2C12226%2C12227%2C12228%2C12229%2C12230%2C12231%2C12232%2C12233%2C12234%2C12235%2C12236%2C12237%2C12238%2C12239%2C12322%2C12329%2C12342%2C12347%2C12349%2C12403%2C12409%2C12410%2C12421%2C12422%2C12423%2C12424%2C12426%2C12427%2C12441%2C12443%2C12463&lineCats=&lines=&allStations=&stations=&selectedStationInfo=&keyword="

AREA_URL_LIST=[
	TOKYO,
	# KANAGAWA,
	# SAITAMA,
	# CHIBA,
]

# ワークブック指定
shisetu_wb=xlwings.Book('施設.xlsx')
kyujin_wb=xlwings.Book('求人.xlsx')
kyuyo_wb=xlwings.Book('給与.xlsx')
# シート指定
sht_shisetu=shisetu_wb.sheets['施設']
sht_kyujin=kyujin_wb.sheets['求人']
sht_kyuyo=kyuyo_wb.sheets['給与']

# ------------------------------
# class
# ------------------------------
class get_url:
	def __init__(self,target_url):
		# URLからソースを取得
		self.bs4obj=BeautifulSoup(requests.get(target_url).text,'html.parser')
		pass
	# 検索結果のページ数を取得
	def page_number(self):
		return int(self.bs4obj.select('ol[class="list-sequence"]')[0].select('li')[3].text)
	# 施設詳細URLを取得
	def shisetu_url(self):
		return [i.get('href') for i in self.bs4obj.select('a') if i.text=="施設詳細"]
	# 求人詳細URLを取得
	def kyujin_url(self):
		kyujin_url_list=[]
		ptr=re.compile('.+?php')
		# 求人URLが無い場合に対応できないので見送り
		# return [ ptr.match(kyujin.select_one('a').get('href')).group() for kyujin in self.bs4obj.select('div[data-kyujin-list]')]
		for kyujin in self.bs4obj.select('div[data-kyujin-list]'):
			# 求人URLが無い場合はpass
			try:
				kyujin_url_list+=[ptr.match(kyujin.a.get('href')).group()]
			except:
				pass
		return kyujin_url_list

class xlsx_entry:
	def __init__(self):
		pass
	# 途中から記入すると重複しそうなのですべて消去
	def init_xlsx(self):
		sht_shisetu.range(2,1).expand('table').clear()
		sht_kyujin.range(2,1).expand('table').clear()
		sht_kyuyo.range(2,1).expand('table').clear()
	# 施設
	def shisetu_url_entry(self,shisetu_url):
		# 既にあるURLの下のセル位置を取得
		if sht_shisetu.range(2,1).value==None:
			shisetu_url_str=sht_shisetu.range(2,1)
		else:
			shisetu_url_str=sht_shisetu.range(sht_shisetu.range(1,1).end("down").row+1,1)
		# URLを記入
		shisetu_url_str.options(transpose=True).value=shisetu_url
	# 求人
	def kyujin_url_entry(self,kyujin_url):
		# 既にあるURLの下のセル位置を取得
		if sht_kyujin.range(2,1).value==None:
			kyujin_url_str=sht_kyujin.range(2,1)
		else:
			kyujin_url_str=sht_kyujin.range(sht_kyujin.range(1,1).end("down").row+1,1)
		# URLを記入
		kyujin_url_str.options(transpose=True).value=kyujin_url
	# 給与
	def kyuyo_url_entry(self,kyujin_url):
		# 既にあるURLの下のセル位置を取得
		if sht_kyuyo.range(2,1).value==None:
			kyuyo_url_str=sht_kyuyo.range(2,1)
		else:
			kyuyo_url_str=sht_kyuyo.range(sht_kyuyo.range(1,1).end("down").row+1,1)
		# URLを記入
		kyuyo_url_str.options(transpose=True).value=kyujin_url

class detail_data:
	def __init__(self):
		# 最後に書き込まれている施設名の1つ下のセル位置を取得
		# 施設
		if sht_shisetu.range(2,2).value==None:
			self.shisetu_detail_str=sht_shisetu.range(2,2)
		else:
			self.shisetu_detail_str=sht_shisetu.range(sht_shisetu.range(1,2).end("down").row+1,2)
		# 求人
		if sht_kyujin.range(2,2).value==None:
			self.kyujin_detail_str=sht_kyujin.range(2,2)
		else:
			self.kyujin_detail_str=sht_kyujin.range(sht_kyujin.range(1,2).end("down").row+1,2)
		# 給与
		if sht_kyuyo.range(2,2).value==None:
			self.kyuyo_detail_str=sht_kyuyo.range(2,2)
		else:
			self.kyuyo_detail_str=sht_kyuyo.range(sht_kyuyo.range(1,2).end("down").row+1,2)
		pass
	# 施設
	def shisetu_detail(self):
		if self.shisetu_detail_str.offset(0,-1).value==None:
			print('施設データを全て取得済みのため終了')
			return
		for shisetu_row in tqdm(range(self.shisetu_detail_str.row,self.shisetu_detail_str.offset(0,-1).end('down').row+1),desc=f"施設"):
		# for shisetu_row in tqdm(range(self.shisetu_detail_str.row,self.shisetu_detail_str.row+11),desc=f"施設"):
			time.sleep(0.1)
			shisetu_url=sht_shisetu.range(shisetu_row,1).value
			bs4obj=BeautifulSoup(requests.get(shisetu_url).text,'html.parser')
			# 掲載終了・ハロワ求人に対応
			# ハロワ求人の場合以外でも em[data-kinmu-koyo-keitai] が無い場合があるので対応
			if 'この求人は募集を終了しているか、非公開求人の可能性があります。' in bs4obj.text or 'お探しのページが見つかりません。' in bs4obj.text:
				sht_shisetu.range(shisetu_row,2).value='削除されたページ'
				# raise Exception('掲載終了ページ')
			else:
				main_contents=bs4obj.main
				# 施設概要文
				sht_shisetu.range(shisetu_row,3).value=main_contents.select('div')[3].text.strip()
				# おすすめ情報
				sht_shisetu.range(shisetu_row,4).value=re.sub('\s{3,}','\n',main_contents.select_one('ul[data-tokucho-list]').get_text('\n').strip())
				for section in main_contents.select('section'):
					if section.h2.text.strip()=='施設概要' or section.h2.text.strip()=='施設詳細':
						for dt in section.select('dt'):
							# textで取得するときにdivを除去、無ければpass、主にGoogleマップ用
							try:
								dt.next_sibling.next_sibling.div.extract()
							except:
								pass
							# Excelの項目名を取得
							excel_item_list=sht_shisetu.range(1,1).expand('right').value
							try:
								# Excelの項目と一致するインデックスを取得
								excel_index=excel_item_list.index(dt.text)
							except:
								# 一致しなければ最後に列を追加してそこに追記
								sht_shisetu.range(1,len(excel_item_list)+1).value=dt.text
								# スペースが3個以上続く場合は改行に置換
								sht_shisetu.range(shisetu_row,len(excel_item_list)+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
							else:
								# あればそこに追記
								# スペースが3個以上続く場合は改行に置換
								sht_shisetu.range(shisetu_row,excel_index+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
	# thread を使用して requests で html を取得して配列に入れる
	def shisetu_detail_thread(self):
		if self.shisetu_detail_str.offset(0,-1).value==None:
			print('施設データを全て取得済みのため終了')
			return
		# shisetu_url_list=sht_shisetu.range(self.shisetu_detail_str.row,1).expand('down').value
		shisetu_url_list=sht_shisetu.range((2,1),(11,1)).value
		with ThreadPoolExecutor() as executor:
			req_res_list=list(executor.map(requests.get,shisetu_url_list))
		for count,req_res in enumerate(tqdm(req_res_list)):
			shisetu_row=self.shisetu_detail_str.row+count
			bs4obj=BeautifulSoup(req_res.text,'html.parser')
			main_contents=bs4obj.main
			# 施設概要文
			sht_shisetu.range(shisetu_row,3).value=main_contents.select('div')[3].text.strip()
			# おすすめ情報
			sht_shisetu.range(shisetu_row,4).value=re.sub('\s{3,}','\n',main_contents.select_one('ul[data-tokucho-list]').get_text('\n').strip())
			for section in main_contents.select('section'):
				if section.h2.text.strip()=='施設概要' or section.h2.text.strip()=='施設詳細':
					for dt in section.select('dt'):
						# textで取得するときにdivを除去、無ければpass、主にGoogleマップ用
						try:
							dt.next_sibling.next_sibling.div.extract()
						except:
							pass
						# Excelの項目名を取得
						excel_item_list=sht_shisetu.range(1,1).expand('right').value
						try:
							# Excelの項目と一致するインデックスを取得
							excel_index=excel_item_list.index(dt.text)
						except:
							# 一致しなければ最後に列を追加してそこに追記
							sht_shisetu.range(1,len(excel_item_list)+1).value=dt.text
							# スペースが3個以上続く場合は改行に置換
							sht_shisetu.range(shisetu_row,len(excel_item_list)+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
						else:
							# あればそこに追記
							# スペースが3個以上続く場合は改行に置換
							sht_shisetu.range(shisetu_row,excel_index+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
	# 求人
	def kyujin_detail(self):
		if self.kyujin_detail_str.offset(0,-1).value==None:
			print('求人データを全て取得済みのため終了')
			return
		for kyujin_row in tqdm(range(self.kyujin_detail_str.row,self.kyujin_detail_str.offset(0,-1).end('down').row+1),desc=f"求人"):
		# for kyujin_row in tqdm(range(self.kyujin_detail_str.row,self.kyujin_detail_str.row+10),desc=f"求人"):
			time.sleep(0.1)
			kyujin_url=sht_kyujin.range(kyujin_row,1).value
			bs4obj=BeautifulSoup(requests.get(kyujin_url).text,'html.parser')
			# 掲載終了・ハロワ求人に対応
			# ハロワ求人の場合以外でも em[data-kinmu-koyo-keitai] が無い場合があるので対応
			if 'この求人は募集を終了しているか、非公開求人の可能性があります。' in bs4obj.text or 'お探しのページが見つかりません。' in bs4obj.text:
				sht_kyujin.range(kyujin_row,2).value='募集終了 or 非公開求人'
				# raise Exception('掲載終了ページ')
			else:
				main_contents=bs4obj.main
				# 配属先
				sht_kyujin.range(kyujin_row,4).value=main_contents.select_one('em[data-tanto-gyomu]').text.strip()
				# 資格
				sht_kyujin.range(kyujin_row,5).value=re.sub('\s{3,}','\n',main_contents.select_one('span[data-shikaku-list]').get_text('\n').strip())
				# おすすめ情報
				sht_kyujin.range(kyujin_row,6).value=re.sub('\s{3,}','\n',main_contents.select_one('ul[data-tokucho-list]').get_text('\n').strip())
				# キャリアパートナーのオススメポイント
				# ハロワ求人の場合とかは無いので、とりあえずtryで
				try:
					sht_kyujin.range(kyujin_row,7).value=main_contents.select_one('div[class="box-message_content"]').get_text('\n').strip()
				except:
					pass
				# section に詳細情報があるので for
				for section in bs4obj.main.select('section'):
					if section.h2.text.strip()=='求人詳細':
						# section の最初の p 要素の概要文を取得
						sht_kyujin.range(kyujin_row,3).value=section.p.get_text('\n').strip()
						# dt に項目名、dd に内容があるので for
						for dt in section.select('dt'):
							# Excelの項目名を取得
							excel_item_list=sht_kyujin.range(1,1).expand('right').value
							try:
								# Excelの項目と一致するインデックスを取得
								excel_index=excel_item_list.index(dt.text)
							except:
								pass
								# 一致しなければ最後に列を追加してそこに追記
								sht_kyujin.range(1,len(excel_item_list)+1).value=dt.text
								# スペースが3個以上続く場合は改行に置換
								sht_kyujin.range(kyujin_row,len(excel_item_list)+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
							else:
								# あればそこに追記
								# スペースが3個以上続く場合は改行に置換
								# 諸手当の場合は無駄に改行が入るので処理追加
								if dt.text=='諸手当':
									sht_kyujin.range(kyujin_row,excel_index+1).value='\n'.join([re.sub('\n{0,}\s{0,}','',i.text.strip()) for i in dt.next_sibling.next_sibling.select('li[class="teate"]')])
								else:
									sht_kyujin.range(kyujin_row,excel_index+1).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
					elif section.h2.text.strip()=='施設情報':
						# dt に項目名、dd に内容があるので for
						for dt in section.select('dt'):
							if dt.text=='施設名':
								# スペースが3個以上続く場合は改行に置換
								sht_kyujin.range(kyujin_row,2).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())
	# 給与
	def kyuyo_detail(self):
		if self.kyuyo_detail_str.offset(0,-1).value==None:
			print('給与データを全て取得済みのため終了')
			return
		for kyuyo_row in tqdm(range(self.kyuyo_detail_str.row,self.kyuyo_detail_str.offset(0,-1).end('down').row+1),desc=f"給与"):
		# for kyuyo_row in tqdm(range(self.kyuyo_detail_str.row,self.kyuyo_detail_str.row+1),desc=f"給与"):
			time.sleep(0.1)
			kyuyo_url=sht_kyuyo.range(kyuyo_row,1).value
			bs4obj=BeautifulSoup(requests.get(kyuyo_url).text,'html.parser')
			# 掲載終了・ハロワ求人に対応
			# ハロワ求人の場合以外でも em[data-kinmu-koyo-keitai] が無い場合があるので対応
			if 'この求人は募集を終了しているか、非公開求人の可能性があります。' in bs4obj.text or 'お探しのページが見つかりません。' in bs4obj.text:
				sht_kyuyo.range(kyuyo_row,2).value='募集終了 or 非公開求人'
				# raise Exception('掲載終了ページ')
			else:
				# em[data-kinmu-koyo-keitai] が有る場合
				try:
					# 勤務時間
					kinmu_jikan_dict={i.th.text.strip():re.sub('\n{1,}\s{0,}','\n',i.td.text.strip()) for i in bs4obj.select_one('div[data-kinmu-jikan-table]').select('tr')}
					# 給与情報
					kyuyo_list=[]
					for kyuyo_joho_obj in bs4obj.select_one('div[data-kyuyo-joho]').select('li'):
						# 雇用形態
						koyo_keitai=kyuyo_joho_obj.select_one('em[data-kinmu-koyo-keitai]').text
						# 資格
						shikau=kyuyo_joho_obj.select_one('span[data-shikaku]').text
						# 勤務時間
						kinmu_jikan=kinmu_jikan_dict.get(koyo_keitai)
						# 給与概要
						kyuyo_summary=('\n'.join([kyuyo_summary_obj.text for kyuyo_summary_obj in kyuyo_joho_obj.select('span[data-kyuyo]')]))
						# 給与詳細
						kyuyo_desc_list=[]
						for kyuyo_desc_obj in kyuyo_joho_obj.select('div[data-kyuyo-description]'):
							kyuyo_desc_list_temp=[]
							# 給与例の名前
							kyuyo_desc_list_temp+=[kyuyo_desc_obj.previous_sibling.previous_sibling.text.strip()]
							# 給与例内容
							kyuyo_desc_list_temp+=[re.sub('\n{2,}','\n',kyuyo_desc_obj.text.strip())]
							# 給与例と内容を改行で区切って配列に入れる
							kyuyo_desc_list+=[('\n'.join(kyuyo_desc_list_temp))]
						# 配列の内容を改行で区切って代入
						kyuyo_desc=('\n\n'.join(kyuyo_desc_list))
						# まとめて配列に入れる
						kyuyo_list+=[koyo_keitai,shikau,kinmu_jikan,kyuyo_summary,kyuyo_desc]
					# リストでExcelに記入
					sht_kyuyo.range(kyuyo_row,3).value=kyuyo_list
				# em[data-kinmu-koyo-keitai] が無い場合
				except:
					# 雇用形態
					sht_kyuyo.range(kyuyo_row,3).value=bs4obj.select_one('div[data-is-mibunka]').em.text.strip()
					# 勤務時間
					sht_kyuyo.range(kyuyo_row,5).value=bs4obj.select_one('div[data-kinmu-jikan-table]').get_text('\n').strip()
					# 給与概要
					sht_kyuyo.range(kyuyo_row,6).value=bs4obj.select_one('div[data-is-mibunka]').div.text.strip()
					# 給与詳細
					sht_kyuyo.range(kyuyo_row,7).value=bs4obj.select_one('div[data-kyuyo-description]').get_text('\n').strip()
				# 施設名
				for section in bs4obj.main.select('section'):
					###
					# continue
					###
					if section.h2.text.strip()=='施設情報':
						# dt に項目名、dd に内容があるので for
						for dt in section.select('dt'):
							if dt.text=='施設名':
								# スペースが3個以上続く場合は改行に置換
								sht_kyuyo.range(kyuyo_row,2).value=re.sub('\s{3,}','\n',dt.next_sibling.next_sibling.get_text('\n').strip())





# ------------------------------
# main
# ------------------------------
xe=xlsx_entry()
dd=detail_data()

def main():
	gu=get_url(CHIBA)
	shisetu_url=gu.shisetu_url()
	kyujin_url=gu.kyujin_url()
	xe.shisetu_url_entry(shisetu_url)
	xe.kyujin_url_entry(kyujin_url)
# main()

# 施設・求人の詳細ページURLを指定したエリアから取得してExcelに入力
def URL_GET():
	xe.init_xlsx()
	for count,AREA_URL in enumerate(AREA_URL_LIST):
		for page in tqdm(range(1,get_url(AREA_URL).page_number()+1),desc=f"{count+1}/{len(AREA_URL_LIST)}"):
		# for page in tqdm(range(1,2+1),desc=f"{count+1}/{len(AREA_URL_LIST)}"):
			gu=get_url(AREA_URL+"&page="+str(page))
			xe.shisetu_url_entry(gu.shisetu_url())
			xe.kyujin_url_entry(gu.kyujin_url())
			# コピーするので省略
			# xe.kyuyo_url_entry(gu.kyujin_url())
			time.sleep(0.1)
# URL_GET()

# 施設・求人・給与データをURLから取得してExcelに入力
def DATA_GET():
	dd.shisetu_detail()
	dd.kyujin_detail()
	dd.kyuyo_detail()
# DATA_GET()

def test02():
	pass
	dd.shisetu_detail_thread()
# test02()

def test04():
	xe.init_xlsx()
	for count,AREA_URL in enumerate(AREA_URL_LIST):
		# for page in tqdm(range(1,get_url(AREA_URL).page_number()+1),desc=f"{count+1}/{len(AREA_URL_LIST)}"):
		# for page in tqdm(range(1,2+1),desc=f"{count+1}/{len(AREA_URL_LIST)}"):
		for page in tqdm(range(1,2),desc=f"{count+1}/{len(AREA_URL_LIST)}"):
			gu=get_url(AREA_URL)
			# xe.shisetu_url_entry(gu.shisetu_url())
			xe.kyujin_url_entry(gu.kyujin_url())
			# xe.kyuyo_url_entry(gu.kyujin_url())
			time.sleep(0.5)
# test04()