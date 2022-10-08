from fastapi import FastAPI

from app.controller.http import router
from app.controller.http.exc_handler import add_exc_handlers

app = FastAPI()

add_exc_handlers(app)
app.include_router(router)
