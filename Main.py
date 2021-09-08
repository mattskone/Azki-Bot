import os
import praw
import 
import MemeSongList as songs

reddit = praw.Reddit(
    client_id = os.environ.get('AZKI_ID'),
    client_secret = os.environ.get('AZKI_SECRET'),
    user_agent = os.environ.get('AZKI_USER_AGENT')) 
subreddit = reddit.subreddit('Hololive')

file = open('VTubers.txt', 'r')
vtuber_list = file.read().split("\n")


# Takes the reddit comment and creates a serch term for YouTube
def createSearch(comment, triggerIndex):
    vtuber = comment[triggerIndex-1]
    song = " ".join(comment[triggerIndex+1:])
    search = vtuber + " / " + song
    return vtuber, song
    
    
def songSearch(title_parts):
    if title_parts[1] == "baka mitai" or title_parts[1] == "bakamitai":
        return songs.bakamitai[title_parts[0]]
    elif title_parts[1] == "unravel":
        return songs.unravel[title_parts[0]]
    else: 
        return None


def writeComment(video):
    if video == None:
        return "I can't seem to find that track. Sorry about that :("
    else:
        return video



for raw_comment in subreddit.stream.comments(): #Grabs every new comment made in the subreddit
    trigger = "play" # If raw_comment does not have this word, ignore it
    comment = raw_comment.body.lower().replace(",", "")
    if f" {trigger} " in comment: # Looks for trigger
        comment_split = comment.split()
        trigger_index = comment_split.index(trigger)
        if comment_split[trigger_index-1] in vtuber_list: # Check if the word before the trigger is a whitelisted VTuber
            key_elements = createSearch(comment_split, trigger_index)
            reply = writeComment(songSearch(key_elements))
            print(comment)
            print(reply)
            
            