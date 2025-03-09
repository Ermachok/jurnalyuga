from fastapi import APIRouter
import feedparser
import re

router = APIRouter(prefix="/api/rss")

RSS_FEED_URL = "https://habr.com/ru/rss/all/all/?limit=100"
REDDIT_RSS_URL = "https://www.reddit.com/r/pugs/top/.rss"


async def get_habr_rss_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    return [
        {
            "title": entry.title,
            "description": entry.summary,
            "link": entry.link,
            "published": entry.published,
        }
        for entry in feed.entries
    ]


async def get_reddit_rss_feed():
    feed = feedparser.parse(REDDIT_RSS_URL)
    news_list = []
    for entry in feed.entries:
        image_url = None
        if 'content' in entry:
            matches = re.findall(r'href="(https://i.redd.it/[^"]+)"', entry.content[0].value)
            if matches:
                image_url = matches[0]

        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "image_url": image_url
        })
    return news_list
