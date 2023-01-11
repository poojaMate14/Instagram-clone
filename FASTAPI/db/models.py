from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class DbUsers(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship('DbPosts', back_populates='author')
    user_comments = relationship('DbComments', back_populates='comment_author')

class DbPosts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('DbUsers', back_populates='posts')
    caption = Column(String)
    image_path = Column(String)
    timestamp = Column(DateTime)
    comments = relationship('DbComments', back_populates='comment_post')

class DbComments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey(DbPosts.id))
    user_id = Column(Integer, ForeignKey(DbUsers.id))
    comment_text = Column(String)
    timestamp = Column(DateTime)
    comment_post = relationship('DbPosts', back_populates='comments')
    comment_author = relationship('DbUsers', back_populates='user_comments')