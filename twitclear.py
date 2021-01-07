import tweepy
import os
from datetime import datetime,timezone

def get_api():
	# get access tokens from environment variable
	consumer_key = os.getenv("CONSUMER_KEY")
	consumer_secret = os.getenv("CONSUMER_SECRET")
	access_token = os.getenv("ACCESS_TOKEN")
	access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

	if (consumer_key is None
		or consumer_secret is None
		or access_token is None
		or access_token_secret is None):
		raise Exception('access tokens have not been set properly')

	# Creating the authentication object
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	# Setting your access token and secret
	auth.set_access_token(access_token, access_token_secret)
	# Creating the API object while passing in auth information
	api = tweepy.API(auth) 
	return api

def clear_tweets(before=7):
	# delete all tweets before a certain number of days past
	api = get_api()
	for page in tweepy.Cursor(api.user_timeline).pages():
		for status in page:
			tid = status._json['id']
			date = status._json['created_at']
			elapsed = datetime.now(timezone.utc) - datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y')
			if elapsed.days >= before:
				api.destroy_status(tid)

def clear_likes(before=7):
	# remove all favorites before a certain number of days past
	api = get_api()
	for page in tweepy.Cursor(api.favorites).pages():
		for status in page:
			tid = status._json['id']
			date = status._json['created_at']
			elapsed = datetime.now(timezone.utc) - datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y')
			if elapsed.days >= before:
				api.destroy_favorite(tid)

if __name__ == '__main__':
	clear_tweets()
	clear_likes()