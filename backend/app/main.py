from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import chat, upload, wife

app = FastAPI()

app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(wife.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "Future Wife API running"}