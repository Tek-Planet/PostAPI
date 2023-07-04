import time
from fastapi import FastAPI, HTTPException, Response, status, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .schemas import CreatePost as Post

from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
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

my_posts = [
    {"title": "First Post", "content": "Conten of first post", "id": 1},
    {"title": "second Post", "content": "Conten of second post", "id": 2}
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# get all post from database


@app.get("/")
def get_posts():
    return {"data": "Welcome to python API course"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

# get a single post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}

# delete post from database


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post from the database

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
