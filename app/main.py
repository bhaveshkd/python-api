from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connectrion was successful")
        break
    except Exception as error:
        print("Database connectrion was not successful")
        print("Error: ", error)
        time.sleep(2)


my_posts = [
    {
        "title": "title of post1",
        "content": "content of post1",
        "id" : 1
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id" : 2
    }
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)

