from fastapi import APIRouter, Request, Depends
import feedparser

router = APIRouter(prefix="/api/rss")

RSS_FEED_URL = "https://habr.com/ru/rss/all/all/"


@router.get("/")
def get_rss_feed(request: Request):
    feed = feedparser.parse(RSS_FEED_URL)
    news_items = []

    for entry in feed.entries:
        news_items.append({
            "title": entry.title,
            "description": entry.description,
            "link": entry.link,
            "published": entry.published,
        })

    return news_items
