# DESCRIPTION

'''This script is designed to post memes from a folder sequentially to Twitter, using captions stored in captions.txt'''

''' Before running this script, one needs to run the mathmemes_6daily_retrieval.py script to download the top 6 posts'''

''' 
1. Loads Twitter credentials and initializes Twitter API
2. Manages the state of posted memes  (last_published.txt)
3. Loads meme data (filenames and captions)
4. Posts memes sequentially
5. Post Process
6. Posting Schedule
'''


import tweepy
import schedule
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter API
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define paths for the folder and files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
math_memes_folder = os.path.join(BASE_DIR, '..', 'math_memes')
captions_file = os.path.join(math_memes_folder, 'captions.txt')
last_published_file = os.path.join(math_memes_folder, 'last_published.txt')

# Function to get the last published meme
def get_last_published_image():
    if os.path.exists(last_published_file):
        with open(last_published_file, 'r') as f:
            last_published = f.read().strip()
    else:
        last_published = None
    return last_published

# Function to update the last published meme
def update_last_published_image(image_name):
    with open(last_published_file, 'w') as f:
        f.write(image_name)

# Function to load captions and meme filenames in order
def load_captions():
    memes = []
    if os.path.exists(captions_file):
        with open(captions_file, 'r') as f:
            for line in f:
                meme_info = line.strip()
                if meme_info:
                    meme_id, meme_caption, *rest = meme_info.split(' - ')
                    meme_filename = f"{meme_id}.jpg"
                    memes.append({
                        'filename': meme_filename,
                        'caption': meme_caption  # Only keep the caption part
                    })
    return memes

# Function to post memes sequentially from the saved list
def post_sequential_meme(job=None):
    all_memes = load_captions()

    # Filter out the memes that have already been posted
    last_published = get_last_published_image()
    if last_published:
        last_published_index = next((i for i, meme in enumerate(all_memes) if meme['filename'] == last_published), -1)
        available_memes = all_memes[last_published_index + 1:]
    else:
        available_memes = all_memes

    if not available_memes:
        print("No more memes left to post.")
        if job:
            schedule.cancel_job(job)  # Cancel the scheduled job
        return False  # Indicate that posting is complete

    # Post the next meme in the list
    next_meme = available_memes[0]
    meme_path = os.path.join(math_memes_folder, next_meme['filename'])

    if os.path.exists(meme_path):
        try:
            # Upload the image to Twitter
            media = api.media_upload(meme_path)
            # Post the tweet with only the caption
            client.create_tweet(text=next_meme['caption'], media_ids=[media.media_id])
            print(f"Posted meme: {next_meme['filename']} with caption: {next_meme['caption']}")

            # Update the last published meme
            update_last_published_image(next_meme['filename'])
        except Exception as e:
            print(f"Error posting meme {next_meme['filename']}: {e}")
    else:
        print(f"File {next_meme['filename']} does not exist.")
    
    return True  # Indicate that there are still memes to post

# Main function to schedule posts for trials
def main():
    all_memes = load_captions()
    
    # If there are no memes to post, exit
    if not all_memes:
        print("No memes found to post.")
        return

    # Post the first meme instantly
    if not post_sequential_meme():
        return  # Exit if no more memes left to post

    # Schedule posting every 10 minutes and pass the job reference
    job = schedule.every(10).minutes.do(lambda: post_sequential_meme(job=schedule.get_jobs()[0]))

    # Run the scheduler
    while True:
        # Run scheduled tasks
        schedule.run_pending()
        # If there are no more jobs left, stop the script
        if not schedule.get_jobs():
            print("No more memes left to post. Stopping.")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()