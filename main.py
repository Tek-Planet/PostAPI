from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/posts")
def read_root():
    return {"Hello": "to classs"}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}
