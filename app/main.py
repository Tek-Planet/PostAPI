import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .routers import post, user, auth
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# connection to database
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="1234", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected ")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def say_hello():
    return {"data": "Welcome to python API course"}
