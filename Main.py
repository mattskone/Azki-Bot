import os

import praw
from apiclient.discovery import build

import MemeSongList as songs


reddit = praw.Reddit(
    client_id=os.environ.get('AZKI_ID'),
    client_secret=os.environ.get('AZKI_SECRET'),
    user_agent=os.environ.get('AZKI_USER_AGENT'),
    username=os.environ.get('BOT_NAME'),
    password=os.environ.get('BOT_PASSWORD')
    )
subreddit = reddit.subreddit('Hololive')

# Using this to test until I'm granted access by r/hololive mods
#subreddit = reddit.subreddit('skoncol17BotTest')

youtube = build('youtube','v3',developerKey=os.environ.get('YOUTUBE_API_KEY'))


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
        
    REQ: Access the keywords/desc of the video to help verify if the
    video is Hololive-related
    TODO: YouTube-related exception handling
    """ 
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
            return item['snippet']['title'], 
                f"https://youtu.be/{item['id']['videoId']}"


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
    
    if video == None:  # Currently does nothing
        return "I can't seem to find that track. Sorry about that :("
    elif request_parts[1] == "bakamitai" or request_parts[1] == "baka mitai":
        return f"[Dame da ne~]({video})"
    elif request_parts[1] == "unravel":
        return f"[This is so sad pien~]({video})"
    else:
        return f"Now playing [{video[0]}]({video[1]})"


file = open('VTubers.txt', 'r')
vtuber_list = file.read().split("\n")

"""TODO: Reddit-related exception handling"""
for raw_comment in subreddit.stream.comments():
    trigger = "play"  # If the comment does not have this word, ignore it
    comment = raw_comment.body.lower().replace(",", "")
    if f" {trigger} " in comment:
        comment_split = comment.split()
        trigger_index = comment_split.index(trigger)
        if comment_split[trigger_index-1] in vtuber_list:  # If it's not a whitelisted VTuber, ignore it
            key_elements = comment_parse(comment_split, trigger_index)
            response = write_reply(key_elements)
            
            #raw_comment.reply(response)
            print(response)