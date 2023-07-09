
from ..database import get_db
from .. import models, schemas, oauth2
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(search)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get a single post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post

# delete post from database


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    # check to ensure only user who created the post can delete it
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"No authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post from the database

@router.put("/{id}", status_code=status.HTTP_201_CREATED,  response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    # check to ensure only user who created the post can delete it
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"No authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
