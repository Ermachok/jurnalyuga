from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_rss_feeds():
    return {"message": "RSS feeds"}


@router.post("/")
def add_rss_feed(feed_url: str):
    return {"message": f"RSS feed {feed_url} added"}
