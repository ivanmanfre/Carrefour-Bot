import tweepy

# Your credentials
api_key = "FtNaa3neJ19FmKfsqLW0gfcyH"
api_key_secret = "ihJIXzAlrqk6TTMALjgay9ddeg9WXKAKxlazmoZwZwe8vHvZzq"
access_token = "798548272256323585-a0bi8sYMSmsZ7lt6FXY5KWpRHZuMARt"
access_token_secret = "VKnT52mdSbKCUw23F883EQaS7sjYIlWdU9k43VvIQWKyN"

client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

try:
    # Create a tweet
    client.create_tweet(text="Hello, world!")
    print("Tweet successfully posted.")
except tweepy.TweepyException as e:
    print(f"Error posting tweet: {e}")