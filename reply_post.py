import praw
import pdb
import re
import os

reddit = praw.Reddit('bot')

if not os.path.isfile('posts_replied_to.txt'):
    posts_replied_to = []
else:
    with open('posts_replied_to.txt', 'r') as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split('\n')
        posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile('comments_read.txt'):
    comments_read = []
else:
    with open('comments_read.txt') as f:
        comments_read = f.read()
        comments_read = comments_read.split('\n')
        comments_read = list(filter(None, comments_read))

subreddit = reddit.subreddit('pythonforengineers')
for submission in subreddit.hot(limit=20):
    if submission.id not in posts_replied_to:
        # Search the submissions title and text
        if re.search("i love python", submission.title, re.IGNORECASE) or re.search('i love python', submission.selftext, re.IGNORECASE):
            submission.reply("Me TOO!!")
            posts_replied_to.append(submission.id)            
        elif re.search("test", submission.title, re.IGNORECASE) or re.search('test', submission.selftext, re.IGNORECASE):
            submission.reply('What are we testing?')
            posts_replied_to.append(submission.id)

        # Remove the "More Comments" comments from the list of comments    
        submission.comments.replace_more(limit=0)

        # Search the submissions comments
        for comment in submission.comments.list():
            if comment.id not in comments_read:
                print(comment.body)
                comments_read.append(comment.id)

with open('posts_replied_to.txt', 'w') as f:
                for post_id in posts_replied_to:
                    f.write(post_id + '\n')
            
with open('comments_read.txt', 'w') as f:
    for comment_id in comments_read:
        f.write(comment_id + '\n')
