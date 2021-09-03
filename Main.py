import os
import praw
import ParseComment

reddit = praw.Reddit(
    client_id = os.environ.get('AZKI_ID'),
    client_secret = os.environ.get('AZKI_SECRET'),
    user_agent = os.environ.get('AZKI_USER_AGENT')) 
subreddit = reddit.subreddit('Hololive')

file = open('Lists\\VTubers.txt', 'r')
vtuber_list = file.read().split("\n")

for raw_comment in subreddit.stream.comments(): #Grabs every new comment made in the subreddit
    trigger = "play" # If raw_comment does not have this word, ignore it
    comment = raw_comment.body.lower().replace(",", "")
    if f" {trigger} " in comment: # Looks for trigger
        comment_split = comment.split()
        trigger_index = comment_split.index(trigger)
        if comment_split[trigger_index-1] in vtuber_list: # Check if the word before the trigger is a whitelisted VTuber
            ParseComment.createSearch(comment_split, trigger_index)