from datetime import timedelta, datetime, timezone
from tweet_loader import TweetApiLoader
from tweet_cleaner import TweetCleaner

should_load_tweets = False
should_clean_tweets = True

def main():
  # Set date_to_use as yesterday
  date_to_use = (datetime.now(timezone.utc) - timedelta(1))

  if should_load_tweets:
    tweet_loader = TweetApiLoader("data/handles.json", date_to_use)
    tweet_loader.load_tweets()

  if should_clean_tweets:
    tweet_cleaner = TweetCleaner(date_to_use)
    tweet_cleaner.create_cleaned_tweets()

if __name__ == "__main__":
    main()