from datetime import timedelta, datetime, timezone
from tweet_loader import TweetApiLoader

def main():
  # Set date_to_use as yesterday
  date_to_use = (datetime.now(timezone.utc) - timedelta(1))
  tweet_loader = TweetApiLoader("data/handles.json", date_to_use)
  tweet_loader.load_tweets()

if __name__ == "__main__":
    main()