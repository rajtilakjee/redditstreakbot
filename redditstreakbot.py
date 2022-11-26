import requests
import pandas as pd
import praw

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    password='',
    user_agent="",
    username='',
)

username = input("Enter your Reddit username: ")

url = 'https://api.pushshift.io/reddit/comment/search?&limit=0&author=' + username + '&after=7d&metadata=true'
data = requests.get(url)
df = pd.json_normalize(data.json()['metadata'])
dn = (df['total_results'])
totalComments = dn[0]

totalUpvotes = 0
for comment in reddit.redditor(username).comments.new(limit=dn[0]):
    totalUpvotes = totalUpvotes + (comment.score)
    
print("Your total comments for the past 7 days are: ", totalComments)
print("Total upvotes on your comments for the past 7 days are: ", totalUpvotes)
