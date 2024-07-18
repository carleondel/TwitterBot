import tweepy
import random
import schedule
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# credentials to access Twitter API

API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


# create an OAuthHandler instance
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

# Función para tuitear una imagen aleatoria
def tweet_random_image():
    meme_folder = 'memes'
    meme_files = os.listdir(meme_folder)
    random_meme = random.choice(meme_files)
    meme_path = os.path.join(meme_folder, random_meme)
    
    try:
        # Subir la imagen
        media = api.media_upload(meme_path)
        # Crear el tweet con la imagen
        client.create_tweet(media_ids=[media.media_id])
        print(f"Publicado: {meme_path}")
    except Exception as e:
        print(f"Error al publicar el tweet: {e}")

# Función principal
def main():
    tweet_random_image()

# Llamar a la función principal
if __name__ == "__main__":
    main()