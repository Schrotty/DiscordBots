import os
import threading
from queue import Queue

from dotenv import load_dotenv, find_dotenv
from extension.twitter.twitter_crawler import fetch_tweets, tweet_handler


def setup(bot):
    if load_dotenv(find_dotenv(f"configuration/.{os.getenv('ENVIRONMENT')}.env")):
        q = Queue()
        threading.Thread(target=fetch_tweets, args=(q,)).start()
        tweet_handler.start(bot, q)
