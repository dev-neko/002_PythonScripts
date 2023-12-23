import json

def tiktok_json_load():
	with open('TikTok_Data_1657155605/user_data.json','r',encoding='utf-8') as f:
		json_load=json.load(f)

		# 保存した音楽
		# ブラウザから保存する方法が分からなかったので保留
		FavoriteSoundList=json_load["Activity"]["Favorite Sounds"]["FavoriteSoundList"]

		# フォローされたアカウント
		FansList=json_load["Activity"]["Follower List"]["FansList"]

		# フォローしたアカウント
		Following=json_load["Activity"]["Following List"]["Following"]

		# 視聴履歴
		ShareHistoryList=json_load["Activity"]["Video Browsing History"]["VideoList"]

		# 保存した動画
		# 1つしか見れなかったのでそれだけいいねした
		FavoriteVideoList=json_load["Activity"]["Favorite Videos"]["FavoriteVideoList"]

		# いいねした動画
		ItemFavoriteList=json_load["Activity"]["Like List"]["ItemFavoriteList"]

		return ItemFavoriteList


def tiktok_json_test():
	with open('TikTok_Data_1657155605/user_data.json','r',encoding='utf-8') as f:
		json_load=json.load(f)

		# いいねした動画
		ItemFavoriteList=json_load["Activity"]["Like List"]["ItemFavoriteList"]

		print(len(ItemFavoriteList))


tiktok_json_test()