import os
import tweepy
import json

def post_tweet():
    # OAuth 2.0 Authentication (current Twitter API v2 standard)
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    # Load tweets from file
    try:
        with open('tweets.txt', 'r', encoding='utf-8') as file:
            tweets = file.readlines()
    except FileNotFoundError:
        print("tweets.txt file not found")
        return
    
    # Load posted tweets
    try:
        with open('posted_tweets.json', 'r') as file:
            posted_tweets = json.load(file)
    except FileNotFoundError:
        posted_tweets = []

    # Find the first tweet that hasn't been posted yet
    tweet_to_post = None
    for tweet in tweets:
        if tweet.strip() not in posted_tweets:
            tweet_to_post = tweet.strip()
            break

    if tweet_to_post:
        try:
            # Create Tweet using v2 endpoint
            response = client.create_tweet(text=tweet_to_post)
            print(f"Successfully posted tweet with ID: {response.data['id']}")
            
            # Add the posted tweet to the list of posted tweets
            posted_tweets.append(tweet_to_post)
            
            # Save the updated list of posted tweets
            with open('posted_tweets.json', 'w') as file:
                json.dump(posted_tweets, file)
            
            # Remove the posted tweet from tweets.txt
            tweets.remove(tweet_to_post + '\n')
            with open('tweets.txt', 'w', encoding='utf-8') as file:
                file.writelines(tweets)
        except tweepy.TweepyException as e:
            print(f"Failed to post tweet: {e}")
    else:
        print("No new tweets to post")

if __name__ == "__main__":
    post_tweet()
