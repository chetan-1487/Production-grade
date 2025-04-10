from fastapi import FastAPI
from app.Router import create_user, post,user_login
from app.Database.models.model import Base
from .Database.database import engine

Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to the YouTube Downloader API",
        "status": "Running"
    }


app.include_router(post.router)
app.include_router(user_login.router)
app.include_router(create_user.router)