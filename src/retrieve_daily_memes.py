# PURPOSE: 

'''1. Fetch top Reddit posts from the previous day:

    Filter posts from the day before.
    Filter posts with a score greater than 150 (unless there are no such posts, in which case it takes at least one).
    Download the images to a folder named memes.'''

import praw
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import requests
import glob

# Load environment variables from .env
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

# Configure Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# Folder to save memes (math_memes')
math_memes_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'math_memes'))
if not os.path.exists(math_memes_folder):
    os.makedirs(math_memes_folder)

# Remove all .jpg files from the folder before downloading new ones
for file_path in glob.glob(os.path.join(math_memes_folder, '*.jpg')):
    try:
        os.remove(file_path)
        print(f"Deleted old meme: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

# Get posts from the previous day
yesterday = datetime.now(timezone.utc) - timedelta(days=1)
start_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=timezone.utc)
end_of_yesterday = start_of_yesterday + timedelta(days=1)

# File to save captions for Twitter posting
captions_file = os.path.join(math_memes_folder, 'captions.txt')

# Open the captions file in write mode
with open(captions_file, 'w') as captions:
    # Fetch top posts from the day before
    ### EDIT SUBREDDIT HERE    -------------------------------------------------------------------
    subreddit = reddit.subreddit('surrealmemes')
    posts_to_save = []
    for submission in subreddit.top(time_filter='day', limit=100): 
        post_date = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
        #print(f"Considering post {submission.id} with score {submission.score} posted on {post_date}")
        
        # Print URL to help debugging if it's an unsupported format
        if not submission.url.endswith(('jpg', 'jpeg', 'png')):
            print(f"Skipping post {submission.id} due to unsupported file type: {submission.url}")
            continue

        if start_of_yesterday <= post_date < end_of_yesterday:
            if submission.score > 150 or len(posts_to_save) < 1:  # At least one post if <150 score
                # If the post has an image
                if submission.url.endswith(('jpg', 'jpeg', 'png')):
                    image_name = f"{submission.id}.jpg"
                    image_path = os.path.join(math_memes_folder, image_name)
                    if not os.path.exists(image_path):  # Avoid downloading duplicates
                        try:
                            response = requests.get(submission.url)
                            with open(image_path, 'wb') as f:
                                f.write(response.content)
                            # Log details to console
                            print(f"Downloaded {image_name}")
                            print(f"Title: {submission.title}")
                            print(f"Score: {submission.score}")
                            print(f"Date: {post_date.strftime('%Y-%m-%d %H:%M:%S')}")
                            print()

                            # Save the caption (title) and other details for future Twitter posting
                            captions.write(f"{submission.id} - {submission.title} - {submission.score} votes - Posted on {post_date.strftime('%Y-%m-%d %H:%M:%S')} UTC\n")

                            posts_to_save.append(submission.title)
                        except Exception as e:
                            print(f"Failed to download {submission.url}: {e}")
        if len(posts_to_save) >= 6:  # Stop when we have 6 posts
            break

if not posts_to_save:
    print("No posts from yesterday meet the criteria.")
