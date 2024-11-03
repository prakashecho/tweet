import os
import tweepy
import json
import time

def post_tweet():
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    try:
        with open('tweets.txt', 'r', encoding='utf-8') as file:
            tweets = file.readlines()
    except FileNotFoundError:
        print("tweets.txt file not found")
        return
    
    try:
        with open('posted_tweets.json', 'r') as file:
            posted_tweets = json.load(file)
    except FileNotFoundError:
        posted_tweets = []

    for tweet in tweets:
        tweet = tweet.strip()
        if tweet not in posted_tweets:
            try:
                # Add a timestamp to make the tweet unique
                unique_tweet = f"{tweet} (Posted at: {time.strftime('%Y-%m-%d %H:%M:%S')})"
                response = client.create_tweet(text=unique_tweet)
                print(f"Successfully posted tweet with ID: {response.data['id']}")
                
                posted_tweets.append(tweet)
                with open('posted_tweets.json', 'w') as file:
                    json.dump(posted_tweets, file)
                
                tweets.remove(tweet + '\n')
                with open('tweets.txt', 'w', encoding='utf-8') as file:
                    file.writelines(tweets)
                
                break  # Exit after successfully posting a tweet
            except tweepy.TweepyException as e:
                if "duplicate content" in str(e).lower():
                    print(f"Tweet is a duplicate, trying next tweet")
                else:
                    print(f"Failed to post tweet: {e}")
                    break  # Exit if there's an error other than duplicate content
    else:
        print("No new tweets to post")

if __name__ == "__main__":
    post_tweet()
