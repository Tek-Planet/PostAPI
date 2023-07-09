from fastapi import FastAPI
from . import models
from .routers import post, user, auth
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# connection to database


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def say_hello():
    return {"data": "Welcome to python API course"}
