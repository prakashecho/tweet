import os
import tweepy

# OAuth 1.0a Authentication
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)

# Load tweets from file
with open('tweets.txt', 'r') as file:
    tweets = file.readlines()

# Post first tweet and remove it from the file
if tweets:
    tweet = tweets[0].strip()
    
    try:
        response = api.update_status(tweet)
        print(f"Successfully posted tweet: {response.text}")
        
        # Update the file to remove the posted tweet
        with open('tweets.txt', 'w') as file:
            file.writelines(tweets[1:])
    except tweepy.TweepyException as e:
        print(f"Failed to post tweet: {e}")
