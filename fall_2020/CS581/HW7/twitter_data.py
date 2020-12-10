#   Author: Ali Kolenovic

#  This program accesses data from a twitter user site

#  To run in a terminal window:   python3  twitter_data.py

import tweepy

### PUT AUTHENTICATION KEYS HERE ###

CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Authentication

authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#  use wait_on_rate_limit to avoid going over Twitter's rate limits
api = tweepy.API(authenticate, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

while True:
    User = input("Enter a Twitter User: ")
    # STOP breaks the loop
    if User.strip() == "STOP":
        break
    else:
        try:
            twitter_user = api.get_user(User)
            # --- Basic accessing fields from User object --- #
            print("Twitter user screen name: ", twitter_user.screen_name)
            print("Twitter user name: ", twitter_user.name)
            print("Twitter user id: ", twitter_user.id)
            print("Twitter user description: ", twitter_user.description)
            print("Twitter user location: ", twitter_user.location)
            print("Twitter user friend count: ", twitter_user.friends_count)
            print("Twitter user follower count: ", twitter_user.followers_count)
            # ----------------------------------------------- #
            print("First 5 Followers")
            # Create a cursor for easy iteration
            cursor = tweepy.Cursor(api.followers, screen_name=twitter_user.screen_name)
            # Create a list to number everything easier
            followers = [follower.screen_name for follower in cursor.items(5)]
            for idx, follower in enumerate(followers):
                print("Follower " + str(idx + 1) + ": ", follower)
            cursor2 = tweepy.Cursor(api.user_timeline, screen_name=twitter_user.screen_name)
            tweets = [status for status in cursor2.items(5)]
            for idx, tweet in enumerate(tweets):
                print("TWEET " + str(idx + 1) + ": ", tweet.text, '\n')
        # If an error reports back it will jump down to here.
        except tweepy.TweepError:
            print("Error user was not found.\n")
