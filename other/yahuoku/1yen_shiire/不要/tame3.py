import time
import keyboard
import pyautogui
import pyscreeze
from pyscreeze import ImageNotFoundException
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION=True
from my_module import my_function




exc_seller = "aoto_station、takasago_station、jeeponoff、y_b_r_2010、ixdcu81410、vwgfc32234、fxc5a1958、tutinoko1290、cold_black_1978、fysfc848、hyyib79076、xr_honey08"
jinja_data_exc=[]
exc_seller_list = exc_seller.split('、')
for fo_exc_seller_list in exc_seller_list:
	exc_url = "https://auctions.yahoo.co.jp/seller/" + fo_exc_seller_list
	jinja_data_exc.append({'exc_seller':fo_exc_seller_list,'exc_url':exc_url,})
