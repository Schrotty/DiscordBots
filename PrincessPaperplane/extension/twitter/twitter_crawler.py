import json
import os
from queue import Queue

import requests
from discord import TextChannel
from discord.ext import tasks


def fetch_tweets(queue: Queue):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=attachments.media_keys,author_id&media.fields"
        "=preview_image_url,url&user.fields=id,profile_image_url,username",
        headers={"Authorization": "Bearer {}".format(os.getenv("TWITTER.BEARER.ART"))},
        stream=True,
    )

    status_code = response.status_code
    print(f"> Twitter Crawler Status: {status_code}")
    if status_code == 200:
        for raw_tweet in response.iter_lines():
            if raw_tweet:
                queue.put(json.loads(str(raw_tweet, "utf-8")))


@tasks.loop(seconds=int(os.getenv("TWITTER.TIMER", 60)))
async def tweet_handler(bot, queue: Queue):
    channel: TextChannel = bot.get_channel(id=int(os.getenv("TWITTER.CHANNEL.CONFIRM")))
    if queue.qsize() > 0:
        tweet = queue.get(False)

        author = tweet["includes"]["users"][0]["username"]
        await channel.send(f"https://twitter.com/{author}/status/{tweet['data']['id']}")
