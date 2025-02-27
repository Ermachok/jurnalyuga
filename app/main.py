from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import user

app = FastAPI(title="Jurnalyuga API", redirect_slashes=True)

app.include_router(user.router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
