import os
from mutagen.easyid3 import EasyID3
import pathlib
import glob
import re
import pprint



a=["苫米地英人 ダヴィンチ脳能力開発プログラムＢ（医師・カウンセラー限定セミナー）Vol..mp3.csv","超瞑想力DVD (online-audio-converter.com)_1475850637.mp3.csv","1％の努力で99％の利益を出す「脳のつくり方」 (online-audio-converte.mp3.csv"]

for i in a:
	# print(len(i.replace(".mp3.csv","")))
	print(i[:47])