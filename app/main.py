from fastapi import FastAPI
from .router import post, auth,user_login

app=FastAPI()

@app.get("/")
def user():
    return{"Message":"Successfully completed"}


app.include_router(post.router)
app.include_router(user_login.router)
