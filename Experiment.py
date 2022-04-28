# Just a file to try things in isolation
import os
from apiclient.discovery import build
import requests

youtube_key = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube','v3',developerKey = youtube_key)

id_payload = {'key': youtube_key, 'fields': 'items(id(videoId))', 'part': 'id,snippet', 'q': 'kiara / sparks'}
video_id = requests.get('https://www.googleapis.com/youtube/v3/videos?', id_payload)

print(video_id.content)
'''
request = youtube.search().list(q=f"kiara / sparks", part='id, snippet', type='video', maxResults=1)
result = request.execute()

for item in result['items']:
    video_id = item['id']['videoId']
    payload = {'key': youtube_key, 'id': video_id, 'fields': 'items(snippet(description))', 'part': 'snippet'}
    r = requests.get('https://www.googleapis.com/youtube/v3/videos?', params=payload)
    desc = str(r.content).lower()
    if "kiara" in desc or "hololive" in desc or "cover" in desc:
        print(f"https://youtu.be/{video_id}") # I wish it gave the full url :(
    else:
        print("Not hololive related")
'''