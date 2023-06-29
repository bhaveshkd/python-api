from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional

from app.routers.user import create_user
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).get(vote.post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted for post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} has no vote for post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
        