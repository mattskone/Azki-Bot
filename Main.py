import os
import praw

reddit = praw.Reddit(
    client_id = os.environ.get('AZKI_ID'),
    client_secret = os.environ.get('AZKI_SECRET'),
    user_agent = os.environ.get('AZKI_USER_AGENT')) 
subreddit = reddit.subreddit('Hololive')


for raw_comment in subreddit.stream.comments(): #Grabs every new comment made in the subreddit
    trigger = "play" # If raw_comment does not have this word, ignore it
    comment = raw_comment.body.lower().replace(",", "")
    if f" {trigger} " in comment: # Looks for trigger
        # Check if the word before the trigger is a whitelisted VTuber
        with open('Lists\\VTubers.txt') as vtuber_list:
            comment_split = comment.split()
            if comment_split[comment_split.index(trigger)-1] in vtuber_list.read().split("\n"):
                print(comment)