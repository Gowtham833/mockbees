from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.question import Question
from app.schemas.auth import UserResponse

router = APIRouter()

class ProfileUpdate(BaseModel):
    name: str

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    update_data: ProfileUpdate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    current_user.name = update_data.name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/bookmarks")
def get_bookmarks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
    questions = [b.question for b in bookmarks if b.question]
    return questions

@router.post("/bookmarks/{question_id}")
def toggle_bookmark(
    question_id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()
    
    if bookmark:
        db.delete(bookmark)
        db.commit()
        return {"message": "Bookmark removed"}
    else:
        new_bookmark = Bookmark(user_id=current_user.id, question_id=question_id)
        db.add(new_bookmark)
        db.commit()
        return {"message": "Bookmark added"}
