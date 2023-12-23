# ------------------------------
# ライブラリ
# ------------------------------
# selenium系
import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from seleniumwire import webdriver
# 他
import os
import zipfile


# ------------------------------
# selenium
# ------------------------------
class Custom_Selenium_bk01():
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

	def sute_driver(self):
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
		# proxy_server='150.230.198.240'
		# proxy_port='3128'
		# chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")

		# driver=webdriver.Chrome(self.CDM_INST,seleniumwire_options=proxy_options)
		# driver=webdriver.Chrome(self.CDM_INST,options=chrome_options,seleniumwire_options=proxy_options)
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)
		# driver=webdriver.Chrome(options=chrome_options,seleniumwire_options=proxy_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(30)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(5)

		# ウィンドウサイズを予め右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		return driver

	def okaneko_driver(self):
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
		proxy_server='103.78.188.126'
		proxy_port='8000'
		# chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")
		# socks5→http接続になる
		# chrome_options.add_argument(f'--proxy-server=socks5h://{proxy_server}:{proxy_port}')
		# 認証
		proxy_id='0gvM5Q'
		proxy_pw='1eySUJ'
		# chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")
		# chrome_options.add_argument(f'--proxy-auth={proxy_id}:{proxy_pw}')

		proxy_options={
			'proxy':{
				'http':f'http://{proxy_id}:{proxy_pw}@{proxy_server}:{proxy_port}',
				'https':f'https://{proxy_id}:{proxy_pw}@{proxy_server}:{proxy_port}',
				'no_proxy':'localhost,127.0.0.1'
			}
		}

		# driver=webdriver.Chrome(self.CDM_INST,seleniumwire_options=proxy_options)
		# driver=webdriver.Chrome(self.CDM_INST,options=chrome_options,seleniumwire_options=proxy_options)
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(30)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(30)

		return driver


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

	def sute_driver(self):
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
		# proxy_server='150.230.198.240'
		# proxy_port='3128'
		# chrome_options.add_argument(f"--proxy-server=http://{proxy_server}:{proxy_port}")

		# driver=webdriver.Chrome(self.CDM_INST,seleniumwire_options=proxy_options)
		# driver=webdriver.Chrome(self.CDM_INST,options=chrome_options,seleniumwire_options=proxy_options)
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)
		# driver=webdriver.Chrome(options=chrome_options,seleniumwire_options=proxy_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)

		# ウィンドウサイズを予め右半分にする
		driver.set_window_size(654,664)
		driver.set_window_position(633,0)

		return driver

	def okaneko_driver_bk01(self):
		chrome_options=webdriver.ChromeOptions()
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option('detach',True)
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		# chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		# chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
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
		# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')

		#############
		# proxy STR #
		#############

		PROXY_HOST='103.78.188.126'
		PROXY_PORT='8000'
		PROXY_USER='0gvM5Q'
		PROXY_PASS='1eySUJ'

		manifest_json="""
		{
		    "version": "1.0.0",
		    "manifest_version": 2,
		    "name": "Chrome Proxy",
		    "permissions": [
		        "proxy",
		        "tabs",
		        "unlimitedStorage",
		        "storage",
		        "<all_urls>",
		        "webRequest",
		        "webRequestBlocking"
		    ],
		    "background": {
		        "scripts": ["background.js"]
		    },
		    "minimum_chrome_version":"22.0.0"
		}
		"""

		background_js="""
		var config = {
		        mode: "fixed_servers",
		        rules: {
		        singleProxy: {
		            scheme: "http",
		            host: "%s",
		            port: parseInt(%s)
		        },
		        bypassList: ["localhost"]
		        }
		    };

		chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

		function callbackFn(details) {
		    return {
		        authCredentials: {
		            username: "%s",
		            password: "%s"
		        }
		    };
		}

		chrome.webRequest.onAuthRequired.addListener(
		            callbackFn,
		            {urls: ["<all_urls>"]},
		            ['blocking']
		);
		"""%(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS)

		pluginfile='proxy_auth_plugin.zip'

		with zipfile.ZipFile(pluginfile,'w') as zp:
			zp.writestr("manifest.json",manifest_json)
			zp.writestr("background.js",background_js)
		chrome_options.add_extension(pluginfile)

		# シークレットモードで上記の拡張機能を有効にするプロファイルを読み込む
		chrome_options.add_argument(r'--user-data-dir=C:\Users\YUTAKA\AppData\Local\Google\Chrome\USER_OKANEKO')

		#############
		# proxy END #
		#############

		# driver=webdriver.Chrome(self.CDM_INST,seleniumwire_options=proxy_options)
		# driver=webdriver.Chrome(self.CDM_INST,options=chrome_options,seleniumwire_options=proxy_options)
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)

		return driver

	def okaneko_driver_bk02(self):
		chrome_options=webdriver.ChromeOptions()
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option('detach',True)
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		# chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		# chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.page_load_strategy='none'
		# 2021年12月30日追加
		# chrome_options.add_argument('--allow-running-insecure-content')
		# chrome_options.add_argument('--disable-web-security')
		# chrome_options.add_argument('--lang=ja')
		# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

		#############
		# proxy STR #
		#############

		# PROXY_HOST='103.78.188.126'
		# PROXY_PORT='8000'
		# PROXY_USER='0gvM5Q'
		# PROXY_PASS='1eySUJ'

		PROXY_DATA=[
			{'PROXY_HOST':'103.78.188.126','PROXY_PORT':'8000','PROXY_USER':'0gvM5Q','PROXY_PASS':'1eySUJ'},
			{'PROXY_HOST':'194.53.189.10','PROXY_PORT':'8000','PROXY_USER':'ou7ogG','PROXY_PASS':'ECs4NN'},
		]
		RANODM_PROXY_DATA=random.choice(PROXY_DATA)
		# print(RANODM_PROXY_DATA)

		manifest_json="""
		{
		    "version": "1.0.0",
		    "manifest_version": 2,
		    "name": "Chrome Proxy 01",
		    "permissions": [
		        "proxy",
		        "tabs",
		        "unlimitedStorage",
		        "storage",
		        "<all_urls>",
		        "webRequest",
		        "webRequestBlocking"
		    ],
		    "background": {
		        "scripts": ["background.js"]
		    },
		    "minimum_chrome_version":"22.0.0"
		}
		"""

		background_js="""
		var config = {
		        mode: "fixed_servers",
		        rules: {
		        singleProxy: {
		            scheme: "http",
		            host: "%s",
		            port: parseInt(%s)
		        },
		        bypassList: ["localhost"]
		        }
		    };

		chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

		function callbackFn(details) {
		    return {
		        authCredentials: {
		            username: "%s",
		            password: "%s"
		        }
		    };
		}

		chrome.webRequest.onAuthRequired.addListener(
		            callbackFn,
		            {urls: ["<all_urls>"]},
		            ['blocking']
		);
		"""%(
			RANODM_PROXY_DATA['PROXY_HOST'],
			RANODM_PROXY_DATA['PROXY_PORT'],
			RANODM_PROXY_DATA['PROXY_USER'],
			RANODM_PROXY_DATA['PROXY_PASS']
		)

		pluginfile='proxy_auth_plugin.zip'

		# with zipfile.ZipFile(pluginfile,'w') as zp:
		# 	zp.writestr("manifest.json",manifest_json)
		# 	zp.writestr("background.js",background_js)
		# chrome_options.add_extension(pluginfile)

		# シークレットモードで上記の拡張機能を有効にするプロファイルを読み込む
		chrome_options.add_argument(r'--user-data-dir=C:\Users\YUTAKA\AppData\Local\Google\Chrome\USER_OKANEKO')

		#############
		# proxy END #
		#############

		# driver=webdriver.Chrome(self.CDM_INST,seleniumwire_options=proxy_options)
		# driver=webdriver.Chrome(self.CDM_INST,options=chrome_options,seleniumwire_options=proxy_options)
		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)

		return driver

	def okaneko_driver(self):
		chrome_options=webdriver.ChromeOptions()
		# アダプタエラー、自動テスト…、を非表示
		chrome_options.add_experimental_option('detach',True)
		chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
		# chrome_options.add_argument('--headless')  #ヘッドレスモード
		chrome_options.add_argument('--incognito')  #シークレットモード
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--disable-desktop-notifications')
		# chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')
		# chrome_options.add_argument('--disable-application-cache')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.page_load_strategy='none'
		# 2021年12月30日追加
		# chrome_options.add_argument('--allow-running-insecure-content')
		# chrome_options.add_argument('--disable-web-security')
		# chrome_options.add_argument('--lang=ja')
		# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示

		# インストールした拡張機能をシークレットモードで有効にするプロファイルを読み込む
		chrome_options.add_argument(r'--user-data-dir=C:\Users\YUTAKA\AppData\Local\Google\Chrome\USER_OKANEKO')
		# chrome_options.add_argument(r'--user-data-dir=C:\Users\ISDYTK\AppData\Local\Google\Chrome\USER_OKANEKO')

		driver=webdriver.Chrome(self.CDM_INST,options=chrome_options)

		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		#要素が見つかるまで指定した時間まで待機
		driver.implicitly_wait(60)

		return driver
