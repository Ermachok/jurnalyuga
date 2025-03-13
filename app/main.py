from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.endpoints import pages, rss, user

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router)
app.include_router(rss.router)
app.include_router(pages.router)

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
