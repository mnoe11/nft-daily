import json
import yaml
import datetime
import os
from dateutil import tz
from datetime import timedelta, datetime, timezone

import requests

'''
Loads tweets for the specified list of twitter
handles.
'''

CONFIG_FILE = "config.yaml"
FULL_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
Y_M_D_DATE_FORMAT = "%Y-%m-%d"


class TweetApiLoader:
  def __init__(self, handle_file_name, date_to_use):
    print("Initializing new TweetLoader")
    self.handle_file_name = handle_file_name

    # Load bearer token from the config file
    with open(CONFIG_FILE) as config_file:
      config_yaml = yaml.safe_load(config_file)
      self.bearer_token = config_yaml["search_tweets_api"]["bearer_token"]

    self.date_to_load = date_to_use

  def __load_handles(self):
    with open(self.handle_file_name) as handle_file:
      return json.load(handle_file)

  # Generates the search tweets url for the given handle
  def __construct_search_tweets_url(self, handle):
    max_results = 100

    # Get only tweets for the 24 hours of the date_to_load
    start_date_time = datetime(
      self.date_to_load.year,
      self.date_to_load.month,
      self.date_to_load.day,
      tzinfo=tz.tzutc())
    end_date_time = start_date_time + timedelta(1)
    start_time = start_date_time.strftime(FULL_DATE_FORMAT)
    end_time = end_date_time.strftime(FULL_DATE_FORMAT)
    print("Generating search URL from {} to {}".format(
      start_date_time.strftime(Y_M_D_DATE_FORMAT),
      end_date_time.strftime(Y_M_D_DATE_FORMAT)))

    # Create URL
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(handle)
    start_time = "start_time={}".format(start_time)
    end_time = "end_time={}".format(end_time)
    tweet_fields = "tweet.fields=text,author_id,created_at,referenced_tweets,entities"
    user_fields = "user.fields=name,username"
    expansions = "expansions=author_id,entities.mentions.username"
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}&{}&{}&{}&{}".format(
        mrf, q, expansions, start_time, end_time, tweet_fields, user_fields
    )
    return url

  # Retrieves the 24 hours of tweets on the date stored in date_to_load for the given handle
  def __get_24_hour_tweets(self, handle):
    api_url = self.__construct_search_tweets_url(handle)
    print("Getting tweets for {}".format(handle))
    headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
    response = requests.request("GET", api_url, headers=headers).json()

    # Get the user metadata out of the users list, and store as user_metadata for
    # easier access
    user_metadata = {}
    for user in response["includes"]["users"]:
      if user["username"] == handle:
        user_metadata = user

    if not "username" in user_metadata:
      raise Exception("No user found with handle {}".format(handle))

    response["user_metadata"] = user_metadata
    return response

  def __write_tweets_to_json(self, tweets):
    dir = "data/{}".format(self.date_to_load.strftime(Y_M_D_DATE_FORMAT))
    if not os.path.exists(dir):
      os.makedirs(dir)

    with open("{}/raw_tweets.json".format(dir), "w") as output_file:
      json.dump(tweets, output_file)


  # Loads all tweets from the API for this TweetApiLoader instance
  def load_tweets(self):
    handles = self.__load_handles()

    tweets = []
    for handle in handles:
      tweets.append(self.__get_24_hour_tweets(handle))

    self.__write_tweets_to_json(tweets)

