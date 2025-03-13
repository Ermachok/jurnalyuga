from fastapi import APIRouter, Request

from app.api.endpoints import rss
from app.dependencies import templates

router = APIRouter()


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/api/users/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/api/users/register")
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/rss_habr")
async def rss_page(request: Request):
    news_list = await rss.get_habr_rss_feed()
    return templates.TemplateResponse(
        "rss_habr.html", {"request": request, "news_list": news_list}
    )


@router.get("/rss_reddit")
async def reddit_rss_page(request: Request):
    news_list = await rss.get_reddit_rss_feed()
    return templates.TemplateResponse(
        "rss_reddit.html", {"request": request, "news_list": news_list}
    )


@router.get("/rss_nyt_sports")
async def nyt_sports_rss_page(request: Request):
    news_list = await rss.get_nyt_sports()
    return templates.TemplateResponse(
        "rss_nyt.html", {"request": request, "news_list": news_list}
    )
