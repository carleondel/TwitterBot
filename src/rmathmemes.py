import praw
import tweepy
import schedule
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales para acceder a la API de Twitter
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Credenciales para acceder a la API de Reddit
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')


# Autenticación con la API de Twitter
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

# Configuración de Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD 
)

def fetch_top_memes():
    subreddit = reddit.subreddit('mathmemes')
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    top_posts = subreddit.top(time_filter='day', limit=100)
    
    valid_posts = []
    for post in top_posts:
        # Asegúrate de que el post tenga más de 150 votos
        if post.score > 150:
            # Añadir fecha de publicación para filtrar por hoy
            post_time = datetime.utcfromtimestamp(post.created_utc)
            if post_time >= one_day_ago:
                valid_posts.append(post)
    
    # Ordenar por votos y seleccionar los 5 mejores
    valid_posts.sort(key=lambda p: p.score, reverse=True)
    top_5_posts = valid_posts[:5] if valid_posts else valid_posts
    return top_5_posts

def tweet_post(post):
    # Asegúrate de que el post tenga un enlace de imagen
    if post.url.endswith(('jpg', 'jpeg', 'png')):
        try:
            # Subir la imagen
            media = api.media_upload(post.url)
            # Crear el tweet con la imagen y el texto del post
            client.create_tweet(
                media_ids=[media.media_id],
                text=f"{post.title}\n\nFuente: {post.url}"
            )
            print(f"Publicado: {post.url} con el caption '{post.title}'")
        except Exception as e:
            print(f"Error al publicar el tweet con la imagen '{post.url}': {e}")

def schedule_tweets(posts):
    # Programar tweets entre 11 AM y 6 PM, separados por 1 hora
    start_time = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    for i, post in enumerate(posts):
        tweet_time = start_time + timedelta(hours=i)
        if tweet_time.hour >= 18:
            break
        schedule.every().day.at(tweet_time.strftime('%H:%M')).do(tweet_post, post=post)

def main():
    posts = fetch_top_memes()
    if not posts:
        print("No se encontraron publicaciones válidas.")
        return

    schedule_tweets(posts)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
