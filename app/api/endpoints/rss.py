from fastapi import APIRouter, Request, Depends
import feedparser

router = APIRouter(prefix="/api/rss")

RSS_FEED_URL = "https://habr.com/ru/rss/all/all/?limit=100"


async def get_rss_feed():
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
