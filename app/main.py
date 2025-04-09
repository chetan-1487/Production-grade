from fastapi import FastAPI
from .router import create_user, post,user_login
from app.model import Base
from .database import engine

Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def root():
    return {"Message": "Successfully completed"}


app.include_router(post.router)
app.include_router(user_login.router)
app.include_router(create_user.router)