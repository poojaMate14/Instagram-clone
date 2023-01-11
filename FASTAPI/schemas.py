from typing import List
from pydantic import BaseModel
from datetime import datetime

class UserRequestBody(BaseModel):
    username: str
    email: str
    password: str

class PostDisplayInsideUser(BaseModel):
    id: int
    caption: str
    timestamp: datetime
    class Config():
        orm_mode = True

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    posts: List[PostDisplayInsideUser] = []
    class Config():
        orm_mode = True

class UserDisplayInsidePost(BaseModel):
    id: int
    username: str
    email: str
    class Config():
        orm_mode = True

class CommentDisplayInsidePost(BaseModel):
    id: int
    comment_text: str
    timestamp: datetime
    comment_author: UserDisplayInsidePost
    class Config():
        orm_mode = True

class PostDisplay(BaseModel):
    id: int
    caption: str
    image_path: str
    timestamp: datetime
    author: UserDisplayInsidePost
    comments: List[CommentDisplayInsidePost] = []
    class Config():
        orm_mode = True

class CommentRequestBody(BaseModel):
    post_id: int
    comment_text: str

class CommentDisplay(BaseModel):
    id: int
    comment_text: str
    timestamp: datetime
    comment_post: PostDisplayInsideUser
    comment_author: UserDisplayInsidePost
    class Config():
        orm_mode = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str
