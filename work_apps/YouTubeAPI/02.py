from pprint import pprint
import requests

api_key='AIzaSyCFeu4f78SDRn5Bjk7l3_XV7dF9FSIgdn0'
user_name='HikakinTV'

def get_channel_info(api_key,user_name):
	channel_url = 'https://www.googleapis.com/youtube/v3/channels'
	param = {'key': api_key,
					 'forUsername': user_name,
					 'part': 'contentDetails',
					# チャンネル名がとりたい場合はsnippet, 登録数がとりたい場合はstatisticsも指定する
					# 'part': 'snippet, contentDetails, statistics'
	}
	req = requests.get(channel_url, params=param)
	return req.json()
def get_playlist_info(api_key,playlist_id, pageToken):
	playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
	param = {'key':api_key,
					 'playlistId': playlist_id,
					 'part': 'contentDetails',
					# 動画のタイトルとかもとりたい場合はsnippetも指定する
					# 'part': 'snippet, contentDetails'
					 'maxResults': '50',
					 'pageToken': pageToken,
	}
	req = requests.get(playlist_url, params=param)
	return req.json()
def get_video_list(api_key,video_id_list):
	video_url = 'https://www.googleapis.com/youtube/v3/videos'
	param = {'key':api_key,
					 'id':','.join(video_id_list),
					 'part':'snippet'
	}
	req = requests.get(video_url, params=param)
	return req.json()

channel_info = get_channel_info(api_key,user_name)
# これを次で使う
playlist_id = channel_info["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
# print(playlist_id)

# 動画IDのリスト格納用の変数
uploaded_video_id_list = []
# pageTokenに空文字列を渡すと何も指定していないのと同じになる
pageToken = ""
while True:
	playlist_result = get_playlist_info(api_key,playlist_id, pageToken)
	# 今までの結果と今回の結果をマージする
	uploaded_video_id_list += [ item["contentDetails"]["videoId"] for item in playlist_result["items"] ]
	# 残りのアイテム数がmaxResultsを超えている場合はnextPageTokenが帰ってくる
	if "nextPageToken" in playlist_result:
		pageToken = playlist_result["nextPageToken"]
	else:
		break

# 取得する動画について順番にAPIを叩いていく
# uploaded_video_id_listにvideo IDが格納されている前提
# maxResultsに合わせて50単位でループを回していく
uploaded_video_name_list=[]
for start_index in range(0, len(uploaded_video_id_list), 50):
	end_index = min(start_index + 50, len(uploaded_video_id_list))
	video_list_result = get_video_list(api_key,uploaded_video_id_list[start_index:end_index])
	# APIの戻り値の["items"]の各要素がそれぞれの動画を表すので、ループ処理する
	for item in video_list_result["items"]:
		# ここでitemを保存したりする
		uploaded_video_name_list+=[item['snippet']['title']]
		# print(item['snippet']['title'])

pprint(uploaded_video_name_list)
print(len(uploaded_video_name_list))