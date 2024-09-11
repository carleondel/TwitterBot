
# SIMPLE SCRIPT TO PRINT DETAILS FROM SUBREDDIT POSTS


import praw
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# We take the top posts all time from a subreddit

# Cargar variables de entorno desde .env
load_dotenv()


# Credenciales para acceder a la API de Reddit
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')



# Configuración de Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD 
)


subreddit = reddit.subreddit('mathmemes')

for submission in subreddit.top(limit=10):
    print(submission.title)
    print('Score:', submission.score)
    print('Url:', submission.url)
    created_utc = submission.created_utc
    created_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print('Date:', created_date)
    print()