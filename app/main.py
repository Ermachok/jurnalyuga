from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import user, rss

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router)
app.include_router(rss.router)

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/users/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/api/users/register")
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get("/rss")
async def rss_page(request: Request):
    news_items = await rss.get_rss_feed()
    return templates.TemplateResponse("rss.html", {"request": request, "news": news_items})
