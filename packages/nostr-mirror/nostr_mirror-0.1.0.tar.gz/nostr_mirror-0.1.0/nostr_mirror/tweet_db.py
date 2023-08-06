class TweetDB:
    """Trivial implementation of a Tweet database.

    We just want to make sure that we don't serve the same Tweet
    twice, and since the RSS feed won't return that many Tweets
    anyways, we can maintain the list of Tweets served in-memory.

    We can make this a proper MySQL database later for persistence.
    """
    def __init__(self, max_tweets=2048):
        self.max_tweets = max_tweets
        self.tweets = []

    def add_tweet(self, tweet_id):
        self.tweets.insert(0, tweet_id)
        while len(self.tweets) > self.max_tweets:
            self.tweets.pop()

    def __contains__(self, item):
        return item in self.tweets
