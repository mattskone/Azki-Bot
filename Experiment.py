# Just a file to try things in isolation
import os
from apiclient.discovery import build

youtube_key = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube','v3',developerKey = youtube_key)

request = youtube.search().list(q=f"Gura / Sparks", part='id, snippet', type='video', maxResults=1)
result = request.execute()
for item in result['items']:
    if "Takanashi Kiara - SPARKS" in item['snippet']['description']:
        print(item['snippet']['description'])
        print(f"https://youtu.be/{item['id']['videoId']}") # I wish it gave the full url :(
    else:
        print("Not hololive related")
        print(f"https://youtu.be/{item['id']['videoId']}")