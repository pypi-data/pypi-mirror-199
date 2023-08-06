import os
import fire
import time

from pynostr.key import PrivateKey
from pynostr.relay_manager import RelayManager

from nostr_mirror.tweet_db import TweetDB
from nostr_mirror.tweet_to_nostr import Tweet2Nostr
from nostr_mirror.twitter_rssbox import TwitterRssBox


# See https://nostr.watch/relays/find for relays
DEFAULT_RELAYS = [
    "wss://relay.damus.io"
]


def main(
    twitter_handle,
    relays=None,
    relay_timeout=6,
    poll_interval_in_sec=300,
    nostr_pk_hex_env="NOSTR_PK_HEX"
):
    # set private key as an environment variable
    private_key = PrivateKey.from_hex(os.environ[nostr_pk_hex_env])

    if relays is None:
        relays = DEFAULT_RELAYS

    # set up relay manager
    relay_manager = RelayManager(timeout=relay_timeout)
    for relay in relays:
        relay_manager.add_relay(relay)

    # set up Twitter RSS feed
    rss = TwitterRssBox(twitter_handle)

    t2n = Tweet2Nostr()
    tdb = TweetDB()

    last_update = None
    backoff = 0
    while True:
        twitter_rss_feed = rss.poll()
        if last_update == twitter_rss_feed.updated:
            # if no updates since last check, then wait before polling again.
            backoff += 1
            time.sleep(poll_interval_in_sec * backoff)
        else:
            backoff = 0
            last_update = twitter_rss_feed.updated

        for tweet in twitter_rss_feed.tweets:
            if tweet.id not in tdb:
                tdb.add_tweet(tweet.id)
                event = t2n.convert(tweet, private_key.public_key.hex())
                event.sign(private_key.hex())
                relay_manager.publish_event(event)

        relay_manager.run_sync()
        time.sleep(poll_interval_in_sec)


if __name__ == "__main__":
    fire.Fire(main)
