import os
import subprocess



p=subprocess.Popen(r"C:\Users\YUTANAO\Documents\プログラム\メモリ開放.bat", stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
print(p.stdout.read())