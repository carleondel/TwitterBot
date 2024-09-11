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
    BEARER_TOKEN,
    API_KEY,
    API_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)


# create a tweet
def tweet_random_number():
    random_number = random.randint(1, 100)
    client.create_tweet(text=str(random_number))

# main function
def main():
    tweet_random_number()

# call main function
if __name__ == "__main__":
    main()