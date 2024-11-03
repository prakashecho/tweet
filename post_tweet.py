import os
import tweepy
import json

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

    posted_new_tweet = False
    tweets_to_remove = []

    for tweet in tweets:
        tweet = tweet.strip()
        if tweet and tweet not in posted_tweets:
            try:
                response = client.create_tweet(text=tweet)
                print(f"Successfully posted tweet: {tweet}")
                print(f"Tweet ID: {response.data['id']}")
                
                posted_tweets.append(tweet)
                tweets_to_remove.append(tweet)
                posted_new_tweet = True
                break  # Exit after successfully posting a tweet
            except tweepy.TweepyException as e:
                if "duplicate content" in str(e).lower():
                    print(f"Tweet is a duplicate, skipping: {tweet}")
                    posted_tweets.append(tweet)
                    tweets_to_remove.append(tweet)
                else:
                    print(f"Failed to post tweet: {e}")
                    break  # Exit if there's an error other than duplicate content
        elif tweet in posted_tweets:
            tweets_to_remove.append(tweet)

    # Update posted_tweets.json
    with open('posted_tweets.json', 'w') as file:
        json.dump(posted_tweets, file)

    # Remove posted and duplicate tweets from tweets.txt
    if tweets_to_remove:
        with open('tweets.txt', 'w', encoding='utf-8') as file:
            file.writelines(tweets)

    if not posted_new_tweet:
        print("No new tweets to post")

if __name__ == "__main__":
    post_tweet()
