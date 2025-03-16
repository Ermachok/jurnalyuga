from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import pages, rss, user, day_word

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router)
app.include_router(rss.router)
app.include_router(pages.router)
app.include_router(day_word.router)

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
