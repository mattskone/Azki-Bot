import os

import praw
import requests
from apiclient.discovery import build

import memesonglist as songs


def comment_parse(comment, trigger_index):
    """
    Returns a list containing the VTuber and the requested song
    
    :param comment: the parsed reddit comment
    :param trigger_index: the... index of the trigger word
        
    REQ: Make some cutoff for the song 
         Currently searches for everything after the trigger
    """

    vtuber = comment[trigger_index-1]
    song = " ".join(comment[trigger_index+1:])
    return vtuber, song

      
def song_search(request_parts):
    """
    Returns the link to a video of the vtuber singing the
    requested song
    
    :param request_parts: A list containing the word before the trigger and
          everything after the trigger
        
    TODO: YouTube-related exception handling
    """ 
    youtube_key = os.environ.get('YOUTUBE_API_KEY')
    youtube = build('youtube','v3',
        developerKey=youtube_key)
        
    if request_parts[1] == "bakamitai" or request_parts[1] == "baka mitai":
        return songs.bakamitai[request_parts[0]]
    elif request_parts[1] == "unravel":
        return songs.unravel[request_parts[0]]
    else:
        request = youtube.search().list(
            q=f"{request_parts[0]} / {request_parts[1]}",
            part='id, snippet', type='video', maxResults=1
            )
        result = request.execute()
        
        for item in result['items']:
            video_id = item['id']['videoId']
            payload = {'key': youtube_key,
                       'id': video_id,
                       'fields': 'items(snippet(description))',
                       'part': 'snippet'
                       }
            r = requests.get('https://www.googleapis.com/youtube/v3/videos?',
                params=payload)
            desc = str(r.content).lower()
            
            if request_parts[0] in desc or "hololive" in desc or "cover" in desc:
                return item['snippet']['title'], f"https://youtu.be/{video_id}"
            else:
                return None


def write_reply(request_parts):
    """
    Writes the reply which will be sent to the commenter
    
    :params request_parts: A list containing the vtuber name and the 
    song being requested

    TODO: Discerne whether a video could not be found because the VTuber
          hasn't sung it, or because the string after the trigger is not
          actually a song
    """
    video = song_search(request_parts)
    
    if video == None:
        return "I can't seem to find that song. Sorry about that :("
    elif request_parts[1] == "bakamitai" or request_parts[1] == "baka mitai":
        return f"[Dame da ne~]({video})"
    elif request_parts[1] == "unravel":
        return f"[This is so sad pien~]({video})"
    else:
        return f"Now playing [{video[0]}]({video[1]})"


def main():
    """TODO: Reddit-related exception handling"""
    reddit = praw.Reddit(
        client_id=os.environ.get('AZKI_ID'),
        client_secret=os.environ.get('AZKI_SECRET'),
        user_agent=os.environ.get('AZKI_USER_AGENT'),
        username=os.environ.get('BOT_NAME'),
        password=os.environ.get('BOT_PASSWORD')
        )
    subreddit = reddit.subreddit('Hololive')
    
    file = open('VTubers.txt')
    vtuber_list = file.read().split("\n")
    
    for raw_comment in subreddit.stream.comments():
        trigger = ", play"  # If the comment does not have this word, ignore it
        comment = raw_comment.body.lower().replace(",", "")
        if f" {trigger} " in comment:
            #import pdb; pdb.set_trace()
            comment_split = comment.split(" ")
            trigger_index = comment_split.index(trigger)
            comment_split[trigger_index-1].replace(",", "")
            if comment_split[trigger_index-1] in vtuber_list:  # If it's not a whitelisted VTuber, ignore it
                key_elements = comment_parse(comment_split, trigger_index)
                response = write_reply(key_elements)
                
                #raw_comment.reply(response)
                print(comment_split)

main()