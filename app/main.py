from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import user, rss, pages

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router)
app.include_router(rss.router)
app.include_router(pages.router)

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
