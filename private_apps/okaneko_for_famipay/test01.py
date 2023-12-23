import random
import time

import winsound

# k = random.randint(ord('あ'),ord('ん'))
# print(chr(k))
#
# k = random.randint(ord('ア'),ord('ン'))
# print(chr(k))


# for i in range(10):
# 	size=random.randint(3,5)
# 	rand_nickname=''.join(chr(random.randint(ord('あ'),ord('ん'))) for _ in range(size))
# 	print(size,rand_nickname)
#
# for i in range(10):
# 	size=random.randint(3,5)
# 	rand_nickname=''.join(chr(random.randint(ord('ア'),ord('ン'))) for _ in range(size))
# 	print(size,rand_nickname)


# size=random.randint(3,5)
# if random.choice(['ひらがな','カタカナ'])=='ひらがな':
# 	rand_nickname=''.join(chr(random.randint(ord('あ'),ord('ん'))) for _ in range(size))
# else:
# 	rand_nickname=''.join(chr(random.randint(ord('ア'),ord('ン'))) for _ in range(size))
# print(rand_nickname)

def winsound_test():
	frequency=500
	duration=500
	for _ in range(2):
		winsound.Beep(frequency, duration)
		time.sleep(1)
# winsound_test()


def proxy_test_01():
	PROXY_DATA=[
		{'PROXY_HOST':'103.78.188.126','PROXY_PORT':'8000','PROXY_USER':'0gvM5Q','PROXY_PASS':'1eySUJ'},
		{'PROXY_HOST':'194.53.189.10','PROXY_PORT':'8000','PROXY_USER':'ou7ogG','PROXY_PASS':'ECs4NN'},
	]

	RANODM_PROXY_DATA=random.choice(PROXY_DATA)
	print(RANODM_PROXY_DATA)
proxy_test_01()