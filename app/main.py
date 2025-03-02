from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import user

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router)

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
