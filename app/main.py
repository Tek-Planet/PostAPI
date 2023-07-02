import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
@app.get("/posts")
def read_root():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


# create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    # commit the changes to database
    conn.commit()

    return {"data": new_post}

# get a single post


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}

# delete post from database


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int):
    cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post from the database

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def create_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE  posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id), ))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return {"data": updated_post}
