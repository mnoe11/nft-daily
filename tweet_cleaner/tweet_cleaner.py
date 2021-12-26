import json
import re

Y_M_D_DATE_FORMAT = "%Y-%m-%d"

class TweetCleaner:
  def __init__(self, date_to_use):
    self.date_to_read = date_to_use.strftime(Y_M_D_DATE_FORMAT)
    print("Initialized Tweet Cleaner for {}".format(self.date_to_read))

  def __load_raw_tweets(self):
    path_to_raw_tweets = "data/{}/raw_tweets.json".format(self.date_to_read)

    with open(path_to_raw_tweets) as raw_tweet_file:
      return json.load(raw_tweet_file)

  '''
  Sanitizes and cleans the text in a tweet
  '''
  def __get_cleaned_tweet_text(self, raw_tweet_text):
    # Removes ampersands and replaces with and
    cleaned_text = raw_tweet_text.replace("&amp;", "and")
    cleaned_text = cleaned_text.replace("\n\n", ". ")
    cleaned_text = cleaned_text.replace("\n", ". ")
    # cleaned_text = re.sub(r"\S*https?:\S*", "", cleaned_text, flags=re.MULTILINE)

    return cleaned_text

  # Gets a cleaned, and more easily consumable form of a tweet
  def __get_cleaned_tweet(self, raw_tweet, user_metadata):
    cleaned_text = self.__get_cleaned_tweet_text(raw_tweet["text"])

    # Tweet Types: quoted, replied_to, tweet
    tweet_type = "tweet"
    referenced_tweet_id = None
    if "referenced_tweets" in raw_tweet:
      # NOTE: There may be the possibility for multiple tweets to occur here, but
      # that is a future enhancement we may make
      referenced_tweet = raw_tweet["referenced_tweets"][0]

      tweet_type = referenced_tweet["type"]
      referenced_tweet_id = referenced_tweet["id"]

    return {
      "tweet_id": raw_tweet["id"],
      "created_at": raw_tweet["created_at"],
      "user_metadata": user_metadata,
      "text": cleaned_text,
      "tweet_type": tweet_type,
      "referenced_tweet_id": referenced_tweet_id
    }

  def __write_cleaned_tweets_to_json(self, cleaned_tweets):
    dir = "data/{}".format(self.date_to_read)

    with open("{}/cleaned_tweets.json".format(dir), "w") as output_file:
      json.dump(cleaned_tweets, output_file)

  def create_cleaned_tweets(self):
    raw_tweet_data = self.__load_raw_tweets()

    cleaned_tweets = []
    for handle in raw_tweet_data:
      user_metadata = handle["user_metadata"]

      for raw_tweet in handle["data"]:
        cleaned_tweets.append(self.__get_cleaned_tweet(raw_tweet, user_metadata))


    self.__write_cleaned_tweets_to_json(cleaned_tweets)
    print("Completed cleaning tweets")