import os
import tweepy
import json

# Authenticate to Twitter
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)

# Load tweets from file
with open('tweets.txt', 'r') as file:
    tweets = file.readlines()

# Post first tweet and remove it from the file
if tweets:
    tweet = tweets[0].strip()
    
    # Use the v2 endpoint to post the tweet
    response = client.create_tweet(text=tweet)
    
    if response.data:
        print(f"Successfully posted tweet: {response.data['text']}")
        
        # Update the file to remove the posted tweet
        with open('tweets.txt', 'w') as file:
            file.writelines(tweets[1:])
    else:
        print("Failed to post tweet:", response)
