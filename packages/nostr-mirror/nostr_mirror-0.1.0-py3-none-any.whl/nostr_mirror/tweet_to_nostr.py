from html.parser import HTMLParser

from pynostr.event import Event

from nostr_mirror.twitter_rss_data import Tweet


class TweetHTMLParser(HTMLParser):
    """Need a way to parse HTML from the RSS feed to something
    renderable on the clients.
    """
    def __init__(self):
        super().__init__()
        self.content = ""

    def handle_data(self, data: str):
        self.content += data


class Tweet2Nostr:

    def convert(self, tweet: Tweet, pubkey: str) -> Event:
        parser = TweetHTMLParser()
        parser.feed(tweet.html)
        parser.close()

        return Event(
            content=parser.content,
            pubkey=pubkey,
        )
