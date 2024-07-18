import tweepy
import schedule
import time
import os

# Credenciales de la API de Twitter
API_KEY = 'TU_API_KEY'
API_SECRET_KEY = 'TU_API_SECRET_KEY'
ACCESS_TOKEN = 'TU_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'TU_ACCESS_TOKEN_SECRET'

# Autenticación con la API de Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def tweet_meme():
    meme_folder = 'memes'
    meme_files = os.listdir(meme_folder)
    meme_path = os.path.join(meme_folder, random.choice(meme_files))
    api.update_with_media(meme_path)
    print(f"Publicado {meme_path}")

# Programar tweets
schedule.every().day.at("10:00").do(tweet_meme)

while True:
    schedule.run_pending()
    time.sleep(1)
