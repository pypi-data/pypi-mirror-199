from dataclasses import dataclass
from typing import List


@dataclass
class Tweet:
    """Example of a Tweet:

    <entry>
        <id>twitter:tweet:1636585410640896000</id>
        <title>the smaller text and spacing on long tweets on iOS looks really nice</title>
        <link href="https://twitter.com/kchro3/status/1636585410640896000" />
        <updated>2023-03-17T04:29:02Z</updated>
        <author><name>kchro3</name></author>
        <content type="html">
        &lt;p>the smaller text and spacing on long tweets on iOS looks really nice&lt;/p>
        </content>
    </entry>
    """
    id: int
    link: str
    updated: int
    author: str
    html: str


@dataclass
class TwitterRssFeed:
    updated: int
    tweets: List[Tweet]
