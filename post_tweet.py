# post_tweet.py
import os
import tweepy

def post_tweet():
    # OAuth 2.0 Authentication (current Twitter API v2 standard)-
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
    
    # Post first tweet and remove it from the file
    if tweets:
        tweet = tweets[0].strip()
        
        try:
            # Create Tweet using v2 endpoint
            response = client.create_tweet(text=tweet)
            print(f"Successfully posted tweet with ID: {response.data['id']}")
            
            # Update the file to remove the posted tweet
            with open('tweets.txt', 'w', encoding='utf-8') as file:
                file.writelines(tweets[1:])
        except tweepy.TweepyException as e:
            print(f"Failed to post tweet: {e}")
    else:
        print("No tweets left in the file")

if __name__ == "__main__":
    post_tweet()
