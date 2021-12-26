from datetime import timedelta, datetime, timezone
from tweet_loader import TweetApiLoader
from tweet_cleaner import TweetCleaner
from tweet_enricher import TweetEnricher

should_load_tweets = False
should_clean_tweets = False
should_enrich_tweets = True

def main():
  # Set date_to_use as yesterday
  date_to_use = (datetime.now(timezone.utc) - timedelta(1))

  if should_load_tweets:
    tweet_loader = TweetApiLoader("data/handles.json", date_to_use)
    tweet_loader.load_tweets()

  if should_clean_tweets:
    tweet_cleaner = TweetCleaner(date_to_use)
    tweet_cleaner.create_cleaned_tweets()

  if should_enrich_tweets:
    tweet_enricher = TweetEnricher(date_to_use)
    tweet_enricher.enrich_tweets()

if __name__ == "__main__":
    main()