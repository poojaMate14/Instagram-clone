from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import posts, users, comments
from auth import authentication
from db import models
from db.database import engine

app = FastAPI()
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount(path='/images', app=StaticFiles(directory='images'), name='images')

models.Base.metadata.create_all(engine)