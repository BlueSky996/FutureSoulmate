from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, upload
from app.services import wife_generator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(wife_generator.router)


app.mount("/images", StaticFiles(directory="app/static/images"), name="images")


@app.get("/")
def home():
    return {"message": "Future Wife API running"}