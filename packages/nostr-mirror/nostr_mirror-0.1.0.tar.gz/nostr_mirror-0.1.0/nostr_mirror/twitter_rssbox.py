from typing import Union, Optional

import datetime
import requests
import xml.etree.ElementTree as ET

from nostr_mirror.twitter_rss_data import Tweet, TwitterRssFeed


class TwitterRssBox:
    """Python wrapper for RSSBox API.

    By default, we can connect to the endpoint in AWS, but we can deploy our own
    RSSBox instance here: https://github.com/stefansundin/rssbox

    I think that Nitter might be better though, since it seems to support long Tweets.
    https://nitter.net/kchro3/rss

    """
    XML_PREFIX = "{http://www.w3.org/2005/Atom}"

    def __init__(self, handle, host_url="https://rssbox.us-west-2.elasticbeanstalk.com"):
        self.handle = handle
        self.host_url = host_url
        self.rss_feed = self._get_rss_feed()

    def poll(self):
        """Polls the RSS feed and checks for new data.

        Still work-in-progress, but the main idea is that we want to know when the
        RSS feed was last updated, and we want to parse out the Tweets from the feed.

        Likely not all Tweet types will be supported initially.

        :return:
        """
        response = requests.get(self.rss_feed)
        assert response.status_code == 200, f"Bad Response: {response.content}"

        root = ET.fromstring(response.content)
        tweets = []
        for child in root:
            parsed = self._parse_xml(child)
            if isinstance(parsed, datetime.datetime):
                updated = round(parsed.timestamp() * 1000)
            elif isinstance(parsed, Tweet):
                tweets.append(parsed)
        return TwitterRssFeed(updated, tweets)

    def _parse_xml(self, node) -> Optional[Union[datetime.datetime, Tweet]]:
        tag = node.tag.replace(self.XML_PREFIX, "")
        if tag == "updated":
            return self._parse_datetime(node.text)
        elif tag == "entry":
            tweet_fields = {}

            for child in node:
                child_tag = child.tag.replace(self.XML_PREFIX, "")
                if child.text:
                    tweet_fields[child_tag] = child.text
                elif child_tag == "link":
                    tweet_fields[child_tag] = child.attrib.get("href")
                elif child_tag == "author":
                    tweet_fields[child_tag] = child[0].text
                else:
                    raise NotImplementedError

            return Tweet(
                id=int(tweet_fields["id"].replace("twitter:tweet:", "")),
                link=tweet_fields["link"],
                updated=self._parse_datetime_to_millis(tweet_fields["updated"]),
                author=tweet_fields["author"],
                html=tweet_fields["content"].replace("&lt;", "<").strip()
            )
        else:
            # ignore other types
            pass

    def _get_rss_feed(self):
        """Gets RSS Feed from RSSBox.

        The RSS URL includes the Twitter User ID and the handle:
            https://rssbox.us-west-2.elasticbeanstalk.com/twitter/{userId}/{handle}

        We can call the RSS Box endpoint that generates the RSS URL suffix
        and prepend it with the host URL.

        :return:
        """
        response = requests.get(
            f"{self.host_url}/twitter",
            params={
                "q": self.handle
            },
            # You may need to fiddle with the HTTP headers or else the API will reject the request.
            # See https://rssbox.us-west-2.elasticbeanstalk.com/ for the actual HTTP request.
            headers={
                "accept": "application/json",
                # NOTE: trailing forward slash needed for successful response
                "referer": f"{self.host_url}/",
                "user-agent": "Mozilla/5.0"
            }
        )

        assert response.status_code == 200, f"Bad Response from {self.host_url}: {response.content}"
        suffix = response.content.decode().replace("\"", "")
        rss_feed = f"{self.host_url}{suffix}"
        return rss_feed

    def _parse_datetime(self, datestring):
        iso = datestring.replace("Z", "+00:00")
        return datetime.datetime.fromisoformat(iso)

    def _parse_datetime_to_millis(self, datestring):
        dt = self._parse_datetime(datestring)
        return round(1000 * dt.timestamp())
