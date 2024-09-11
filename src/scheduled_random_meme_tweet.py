
# RANDOM MEME TWITTER POSTING FROM MEMES FOLDER

import tweepy
import random
import schedule
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales para acceder a la API de Twitter
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

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

# Archivo para llevar el registro de la última imagen publicada

# Definir la ruta absoluta para last_published.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAST_PUBLISHED_FILE = os.path.join(BASE_DIR, 'last_published.txt')

# Función para obtener la última imagen publicada
def get_last_published_image():
    if os.path.exists(LAST_PUBLISHED_FILE):
        with open(LAST_PUBLISHED_FILE, 'r') as f:
            last_published = f.read().strip()
    else:
        last_published = None
    return last_published

# Función para actualizar la última imagen publicada
def update_last_published_image(image_name):
    with open(LAST_PUBLISHED_FILE, 'w') as f:
        f.write(image_name)

# Función para tuitear una imagen aleatoria sin repetición consecutiva
def tweet_random_image():
    meme_folder = 'memes'
    # Filtrar solo archivos con extensiones de imagen válidas
    # Esto lo hacemos porque se generan los zone.identifier en la carpeta de memes
    valid_extensions = ('.jpg', '.jpeg', '.png')
    meme_files = [f for f in os.listdir(meme_folder) if os.path.isfile(os.path.join(meme_folder, f)) and f.lower().endswith(valid_extensions)]

    last_published = get_last_published_image()
    
    # Filtrar para evitar la última imagen publicada
    available_memes = [meme for meme in meme_files if meme != last_published]
    
    if not available_memes:
        print("No quedan imágenes disponibles para tuitear.")
        return
    
    random_meme = random.choice(available_memes)
    meme_path = os.path.join(meme_folder, random_meme)


    print(f"Seleccionada para publicación: {random_meme}")


    try:
        # Subir la imagen
        media = api.media_upload(meme_path)
        # Crear el tweet con la imagen
        client.create_tweet(media_ids=[media.media_id])
        print(f"Publicado: {meme_path}")
        # Actualizar la última imagen publicada
        update_last_published_image(random_meme)
    except Exception as e:
        print(f"Error al publicar el tweet: {e}")

# Función principal
def main():
    # Programar tweets cada 2 minutos
    schedule.every(2).minutes.do(tweet_random_image)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Llamar a la función principal
if __name__ == "__main__":
    main()
