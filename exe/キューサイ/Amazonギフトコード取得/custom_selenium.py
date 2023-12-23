# ------------------------------
# ライブラリ
# ------------------------------
# selenium系
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# ------------------------------
# selenium
# ------------------------------
class Custom_Selenium():
	def __init__(self):
		# chromedriver.exeのインストール先
		self.CDM_INST=ChromeDriverManager().install()

	def qsai_driver(self):
		chrome_options=webdriver.ChromeOptions()
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option('detach',True)
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
		# chrome_options.page_load_strategy='none'
		# 2021年12月30日追加
		# chrome_options.add_argument('--allow-running-insecure-content')
		# chrome_options.add_argument('--disable-web-security')
		# chrome_options.add_argument('--lang=ja')
		# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

		# ブラウザの種類を特定するための文字列
		# 笹澤さんのアプリ
		# USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
		# 前に使っていた
		# USER_AGENT="Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
		# 新しくironで取得した
		# USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Iron Safari/537.36"
		# 新しくchromeで取得した
		# USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
		# USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
		# USER_AGENT='Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0'
		# chrome_options.add_argument(f'--user-agent={USER_AGENT}')
		# proxy
		# proxy_server='141.147.184.254'
		# proxy_port='3128'
		# chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")

		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(30)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(30)

		return driver

	def sute_driver_bk01(self):
		chrome_options=webdriver.ChromeOptions()

		# try:
		# 	# 起動しているdriverを再利用する
		# 	chrome_options.add_argument('--remote-debugging-port=9222')
		# 	# Seleniumでの処理後、Chromeを起動したままにする
		# 	chrome_options.add_experimental_option('detach',True)
		# 	# アダプタエラー、自動テスト…、を非表示
		# 	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# except:
		# 	chrome_options.add_experimental_option('debuggerAddress','127.0.0.1:9222')

		# chrome_options.add_experimental_option('debuggerAddress','127.0.0.1:9222')

		# Seleniumでの処理後、Chromeを起動したままにする
		chrome_options.add_experimental_option('detach',True)
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])

		# chrome_options.add_argument('--remote-debugging-port=9222')

		# その他
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
		# chrome_options.page_load_strategy='none'
		# 2021年12月30日追加
		# chrome_options.add_argument('--allow-running-insecure-content')
		# chrome_options.add_argument('--disable-web-security')
		# chrome_options.add_argument('--lang=ja')
		# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

		# 新しくchromeで取得した
		# USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
		# chrome_options.add_argument(f'--user-agent={USER_AGENT}')

		# proxy
		proxy_server='150.230.198.240'
		proxy_port='3128'
		chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")

		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(30)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(5)

		# ウィンドウサイズを予め右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		return driver

	def sute_driver(self):
		chrome_options=webdriver.ChromeOptions()
		# Seleniumでの処理後、Chromeを起動したままにする
		chrome_options.add_experimental_option('detach',True)
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# その他
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(30)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(5)
		# ウィンドウサイズを予め右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)
		return driver