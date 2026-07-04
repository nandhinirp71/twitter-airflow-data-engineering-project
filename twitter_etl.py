import os

import pandas as pd
import tweepy

from xquik_export import load_xquik_rows


DEFAULT_OUTPUT_PATH = "refined_tweets.csv"
DEFAULT_SCREEN_NAME = "@elonmusk"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _write_tweets(rows, output_path: str):
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df


def run_twitter_etl():
    output_path = os.getenv("TWEET_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    xquik_export_path = os.getenv("XQUIK_EXPORT_PATH")
    if xquik_export_path:
        return _write_tweets(load_xquik_rows(xquik_export_path), output_path)

    access_key = _required_env("TWITTER_ACCESS_KEY")
    access_secret = _required_env("TWITTER_ACCESS_SECRET")
    consumer_key = _required_env("TWITTER_CONSUMER_KEY")
    consumer_secret = _required_env("TWITTER_CONSUMER_SECRET")
    screen_name = os.getenv("TWITTER_SCREEN_NAME", DEFAULT_SCREEN_NAME)
    tweet_count = int(os.getenv("TWITTER_TWEET_COUNT", "200"))

    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=screen_name,
                            # 200 is the maximum allowed count
                            count=tweet_count,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    tweet_rows = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}

        tweet_rows.append(refined_tweet)

    return _write_tweets(tweet_rows, output_path)
