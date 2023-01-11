from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError

from db.database import get_db
from db.models import DbUsers
from helpers.hash import Hash
from schemas import UserDisplay

router = APIRouter(
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = '69ae13e62ccbe48df178853368b64d31863bb9c030173411073cbcaf0fd2ca62'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

@router.post('/token')
def create_access_token(req_body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DbUsers).filter(DbUsers.username == req_body.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username does not exist!'
        )
    if not Hash.verify(req_body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password does not match!'
        )
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        'sub': user.username,
        'exp': expire
    }
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        'access_token': access_token,
        'token_type': 'Bearer',
        'user_id': user.id,
        'username': user.username
    }

@router.get('/authuser', response_model=UserDisplay)
def get_user_by_token(token: str, db: Session = Depends(get_db)):
    return get_current_user(token, db)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = decoded_jwt.get('sub')
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(DbUsers).filter(DbUsers.username == username).first()
    if not user:
        raise credentials_exception
    return user