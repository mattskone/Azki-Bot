import os
import praw
from apiclient.discovery import build
import MemeSongList as songs


reddit = praw.Reddit(
    client_id = os.environ.get('AZKI_ID'),
    client_secret = os.environ.get('AZKI_SECRET'),
    user_agent = os.environ.get('AZKI_USER_AGENT')) 
subreddit = reddit.subreddit('Hololive')

youtube = build('youtube','v3',developerKey = os.environ.get('YOUTUBE_API_KEY'))

'''
Takes the reddit comment picks out the VTuber name and title of song
params:
    - comment: the parsed reddit comment
    - triggerIndex: the... index of the trigger word
return: 
    - A list containing the vtuber name and the song being requested
    
TODO: 
    - Does not work if the comment continues after the request.  Need to make some cutoff for the song
'''
def createSearch(comment, triggerIndex):
    vtuber = comment[triggerIndex-1]
    song = " ".join(comment[triggerIndex+1:])
    return vtuber, song

    
'''
Retreives the link to a video of the vtuber singing the requested song
params:
    - search_parts: A list containing the vtuber name and the song being requested
return:
    - Link to a youtube video
    
TODO:
    - Access the keywords of the video to help verify if the video is Hololive-related
    - Related: Build a system which verifies that the video is actually a song and not some clip or unrelated video
    - Exception handling if bot cannot connect to YouTube
'''    
def songSearch(search_parts):
    if search_parts[1] == "bakamitai" or search_parts[1] == "baka mitai":
        return songs.bakamitai[search_parts[0]]
    elif search_parts[1] == "unravel":
        return songs.unravel[search_parts[0]]
    else: 
        request = youtube.search().list(q=f"{search_parts[0]} / {search_parts[1]}", part='id, snippet', type='video', maxResults=1)
        result = request.execute()
        for item in result['items']:
            return item['snippet']['title'], f"https://youtu.be/{item['id']['videoId']}" # I wish it gave the full url :(


'''
Writes the reply which will be sent to the commenter
params:
    - video: link to a youtube video
    - search_parts: A list containing the vtuber name and the song being requested
return:
    - Message to commenter making the request

TODO:
    - Discerne whether a video could not be found because the VTuber hasn't sung it, or because the string after the trigger is not actually a song
'''
def writeReply(video, search_parts):
    if video == None:
        return "I can't seem to find that track. Sorry about that :("
    elif search_parts[1] == "bakamitai" or search_parts[1] == "baka mitai":
        return f"[Dame da ne~]({video})"
    elif search_parts[1] == "unravel":
        return f"[This is so sad pien~]({video})"
    else:
        return f"Now playing [{video[0]}]({video[1]})"


'''
TODO:
    - Exception handling if reddit servers cannot be reached
    - Execute request even if trigger word appears before request. Ex: "I really wanted to see them play Dead Rising 2.  Coco play Baka Mitai"
'''
file = open('VTubers.txt', 'r')
vtuber_list = file.read().split("\n")

for raw_comment in subreddit.stream.comments(): #Grabs every new comment made in the subreddit
    trigger = "play" # If raw_comment does not have this word, ignore it
    comment = raw_comment.body.lower().replace(",", "") # The correct grammar is <VTuber>, play <Song>.  Even though most people ommit it, a number of people (including me) use it
    if f" {trigger} " in comment: # Looks for trigger
        comment_split = comment.split()
        trigger_index = comment_split.index(trigger)
        if comment_split[trigger_index-1] in vtuber_list: # Check if the word before the trigger is a whitelisted VTuber
            key_elements = createSearch(comment_split, trigger_index)
            response = writeReply(songSearch(key_elements), key_elements)
            #raw_comment.reply(response)    Can't use this until I'm granted permission by Hololive mods
            print(response)
            
            
            