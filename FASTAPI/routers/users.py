from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from schemas import UserRequestBody, UserDisplay
from db.database import get_db
from db.models import DbUsers
from helpers.hash import Hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)

# Get all Users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(DbUsers).all()

# Get User by Id
@router.get('/{id}', response_model=UserDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    found_user = db.query(DbUsers).filter(DbUsers.id == id).first()
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found in db!'
        )
    return found_user

# Create User
@router.post('/', response_model=UserDisplay)
def create_user(req_body: UserRequestBody, db: Session = Depends(get_db)):
    new_user = DbUsers(
        username = req_body.username,
        email = req_body.email,
        password = Hash.bcrypt(req_body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Delete user
@router.delete('/{id}')
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    found_user = db.query(DbUsers).filter(DbUsers.id == id).first()
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found in db!'
        )
    db.delete(found_user)
    db.commit()
    return {
        'msg': f'User {id} deleted successfully!'
    }