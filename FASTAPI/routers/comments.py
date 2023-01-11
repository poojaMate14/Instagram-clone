from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from schemas import CommentRequestBody, CommentDisplay, UserAuth
from db.database import get_db
from db.models import DbComments, DbPosts
from auth.authentication import get_current_user

router = APIRouter(
    prefix='/comments',
    tags=['comments']
)

@router.get('/post/{post_id}', response_model=List[CommentDisplay])
def get_all_commments_by_post_id(post_id: int, db: Session = Depends(get_db)):
    return db.query(DbComments).filter(DbComments.post_id == post_id).all()

@router.get('/{id}', response_model=CommentDisplay)
def get_comment_by_id(id: int, db: Session = Depends(get_db)):
    found_comment = db.query(DbComments).filter(DbComments.id == id).first()
    if not found_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Comment {id} does not exist!'
        )
    return found_comment

@router.post('/', response_model=CommentDisplay)
def create_comment_on_post(req_body: CommentRequestBody, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    found_post = db.query(DbPosts).filter(DbPosts.id == req_body.post_id).first()
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post id {req_body.post_id} does not exist!'
        )

    new_comment = DbComments(
        post_id = req_body.post_id,
        user_id = current_user.id,
        comment_text = req_body.comment_text,
        timestamp = datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.delete('/{id}')
def delete_comment_by_id(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    found_comment = db.query(DbComments).filter(DbComments.id == id).first()
    if not found_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Comment {id} does not exist!'
        )
    if found_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'You are not authorized to delete this comment!'
        )
    db.delete(found_comment)
    db.commit()
    return {
        'msg': f'Comment {id} deleted successfully!'
    }