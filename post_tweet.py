# post_tweet.py
import os
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"])
auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

# Load tweets from file
with open('tweets.txt', 'r') as file:
    tweets = file.readlines()

# Post first tweet and remove it from the file
if tweets:
    tweet = tweets[0].strip()
    api.update_status(tweet)
    
    # Update the file to remove the posted tweet
    with open('tweets.txt', 'w') as file:
        file.writelines(tweets[1:])
