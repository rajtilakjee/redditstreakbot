import praw
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv('API_CLIENT'),
    client_secret=os.getenv('API_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent="Streak Bot for Reddit",
    username=os.getenv('REDDIT_USERNAME'),
    check_for_async=False
)

target_sub = "artofml"
subreddit = reddit.subreddit(target_sub)
trigger_phrase = "!streak"

def getComments(username):
    url = 'https://api.pushshift.io/reddit/comment/search?&limit=0&author=' + username + '&after=7d&metadata=true'
    data = requests.get(url)
    df = pd.json_normalize(data.json()['metadata'])
    dn = (df['total_results'])
    totalComments = dn[0]
    return totalComments

def getUpvotes(username,totalComments):
    totalUpvotes = 0
    for comment in reddit.redditor(username).comments.new(limit=totalComments):
        totalUpvotes = totalUpvotes + (comment.score)
    return totalUpvotes

for comment in subreddit.stream.comments(skip_existing=True):  
    if trigger_phrase in comment.body:  
        author = str(comment.author)
        totalComments = getComments(author)
        totalUpvotes = getUpvotes(author,totalComments)
        comment.reply("Total number of comments you made in the last 7 days: " + str(totalComments) + " " + "Total upvotes your comments received in the last 7 days: " + str(totalUpvotes))
