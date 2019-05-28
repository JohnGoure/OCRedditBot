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

subreddit = reddit.subreddit('pythonforengineers')
for submission in subreddit.hot(limit=5):
    if submission.id not in posts_replied_to:
        if re.search("i love python", submission.title, re.IGNORECASE) or re.search('i love python', submission.description, re.IGNORECASE):
            submission.reply("Me TOO!!")
            posts_replied_to.append(submission.id)
            with open('posts_replied_to.txt', 'w') as f:
                for post_id in posts_replied_to:
                    f.write(post_id + '\n')
        elif re.search("test", submission.title, re.IGNORECASE) or re.search('test', submission.description, re.IGNORECASE):
            submission.reply('What are we testing?')
            posts_replied_to.append(submission.id)
            with open('posts_replied_to.txt', 'w') as f:
                for post_id in posts_replied_to:
                    f.write(post_id + '\n')

print(f'Connected to sub-reddit {reddit.subreddit.displayname}.')
