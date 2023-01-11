import shutil
import string
import random
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm.session import Session

from schemas import PostDisplay, UserAuth
from db.database import get_db
from db.models import DbPosts
from auth.authentication import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

# Get all Posts
@router.get('/', response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(DbPosts).all()

# Get Post by Id
@router.get('/{id}', response_model=PostDisplay)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    found_post = db.query(DbPosts).filter(DbPosts.id == id).first()
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post {id} not found in db!'
        )
    return found_post

# Create Post
@router.post('/', response_model=PostDisplay)
def create_post(caption: str, image: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    new_post = DbPosts(
        user_id = current_user.id,
        caption = caption,
        image_path = get_image_path(image),
        timestamp = datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Delete Post
@router.delete('/{id}')
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    found_post = db.query(DbPosts).filter(DbPosts.id == id).first()
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post {id} not found in db!'
        )
    if found_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'You are not authorized to delete this post!'
        )
    db.delete(found_post)
    db.commit()
    return {
        'msg': f'Post {id} deleted successfully!'
    }

def get_image_path(image: UploadFile):
    rand_str = ''.join(random.choice(string.ascii_letters) for i in range(6))
    rand_str = '_' + rand_str + '.'
    image_rand_filename = rand_str.join(image.filename.rsplit('.', 1))
    path = f'images/{image_rand_filename}'
    with open(path, 'w+b') as write_file:
        shutil.copyfileobj(image.file, write_file)
    return path
