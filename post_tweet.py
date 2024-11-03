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

    for tweet in tweets:
        tweet = tweet.strip()
        if tweet not in posted_tweets:
            try:
                response = client.create_tweet(text=tweet)
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
                    print(f"Tweet is a duplicate, skipping: {tweet}")
                    posted_tweets.append(tweet)  # Add to posted tweets to avoid trying again
                    with open('posted_tweets.json', 'w') as file:
                        json.dump(posted_tweets, file)
                    tweets.remove(tweet + '\n')
                    with open('tweets.txt', 'w', encoding='utf-8') as file:
                        file.writelines(tweets)
                else:
                    print(f"Failed to post tweet: {e}")
                    break  # Exit if there's an error other than duplicate content
    else:
        print("No new tweets to post")

if __name__ == "__main__":
    post_tweet()
