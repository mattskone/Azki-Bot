# Just a file to try things in isolation
import os
from apiclient.discovery import build

youtube_key = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube','v3',developerKey = youtube_key)

request = youtube.search().list(q=f"Gura / King", part='id, snippet', type='video', maxResults=1)
result = request.execute()
for item in result['items']:
    print(item['snippet']['title'])
    print(f"https://youtu.be/{item['id']['videoId']}") # I wish it gave the full url :(