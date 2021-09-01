import os
import praw
from dotenv import load_dotenv

load_dotenv('Credentials.env')

reddit = praw.Reddit(
    client_id = os.environ.get('CLIENT_ID'),
    client_secret = os.environ.get('CLIENT_SECRET'),
    user_agent = os.environ.get('USER_AGENT'))
    
subreddit = reddit.subreddit('Hololive')


trigger = "play" # The substring the bot is looking for

for comment in subreddit.stream.comments(): #Grabs every new comment made in the subreddit
    comment_lower = comment.body.lower()
    if f" {trigger} " in comment_lower: # Looks for trigger
        # Check if the word before the trigger is a whitelisted VTuber
        with open('Lists\\VTubers.txt') as vtuber_list:
            comment_split = comment_lower.split()
            if comment_split[comment_split.index(trigger)-1] in vtuber_list.read():
                print(comment_lower)
