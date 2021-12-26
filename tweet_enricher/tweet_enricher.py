import json
import re

Y_M_D_DATE_FORMAT = "%Y-%m-%d"

'''
Can be used to enrich clean tweet data. Enrichment methods
include simple enrichment (such as mentioned tokens) and more
advanced enrichment using Cloud NLP
'''
class TweetEnricher:
  def __init__(self, date_to_use):
    self.date_to_read = date_to_use.strftime(Y_M_D_DATE_FORMAT)
    print("Initialized Tweet Enricher for {}".format(self.date_to_read))

  def __load_cleaned_tweets(self):
    path_to_cleaned_tweets = "data/{}/cleaned_tweets.json".format(self.date_to_read)

    with open(path_to_cleaned_tweets) as cleaned_tweet_file:
      return json.load(cleaned_tweet_file)

  def __write_enriched_tweets_to_json(self, enriched_tweets):
    dir = "data/{}".format(self.date_to_read)

    with open("{}/enriched_tweets.json".format(dir), "w") as output_file:
      json.dump(enriched_tweets, output_file)

  # Filter out replies and quote tweets
  # NOTE: We may want to start taking these into consideration in the future
  #       but for now we hold off
  def __get_cleaned_tweets_to_use(self, cleaned_tweets):
    regular_tweets = []
    for cleaned_tweet in cleaned_tweets:
      if cleaned_tweet["tweet_type"] == "tweet":
        regular_tweets.append(cleaned_tweet)

    return regular_tweets

  def __get_tokens_in_tweet(self, tweet_text):
    token_pattern = '[$][a-zA-Z]+'
    tokens = re.findall(token_pattern, tweet_text)

    token_set = set()
    for token in tokens:
      upper_token = token.upper().strip()
      token_set.add(upper_token)
    return list(token_set)

  # Enriches the tweets using AWS
  def __get_enriched_tweets(self, cleaned_tweets):
    tweets_to_use = self.__get_cleaned_tweets_to_use(cleaned_tweets)

    enriched_tweets = []
    for tweet_to_use in tweets_to_use:

      enriched_tweet = tweet_to_use
      enriched_tweet["tokens"] = self.__get_tokens_in_tweet(tweet_to_use["text"])
      enriched_tweets.append(enriched_tweet)

    return enriched_tweets

  def enrich_tweets(self):
    cleaned_tweets = self.__load_cleaned_tweets()

    enriched_tweets = self.__get_enriched_tweets(cleaned_tweets)

    self.__write_enriched_tweets_to_json(enriched_tweets)
    print("Completed enriching tweets")