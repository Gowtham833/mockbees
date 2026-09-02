from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse
import json
import time
import threading
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.test_attempt import TestConfigRequest, TestAttemptResponse, TestResultResponse, AnswerSubmission, SubmitTestRequest
from app.services.exam_service import get_exam_by_id, create_test_attempt, get_test_attempt, save_answer, submit_test
from app.services.ai_service import generate_questions

router = APIRouter()

@router.post("/generate", response_model=TestAttemptResponse)
def generate_mock_test(
    config: TestConfigRequest,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    exam = get_exam_by_id(db, config.exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
        
    num_q = config.num_questions or exam.total_questions
    
    # Create attempt with status 'PENDING'
    attempt = create_test_attempt(db, current_user.id, exam.id, num_q)
    
    # The generation_worker_loop running in the background will pick this up
    return attempt

@router.get("/history", response_model=List[TestResultResponse])
def get_test_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    from app.models.test_attempt import TestAttempt
    attempts = db.query(TestAttempt).filter(TestAttempt.user_id == current_user.id).order_by(TestAttempt.started_at.desc()).all()
    return attempts

@router.get("/{attempt_id}")
def read_test_attempt(
    attempt_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    attempt = get_test_attempt(db, attempt_id, current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Test attempt not found")
        
    if attempt.status == 'in_progress':
        # hide correct answers
        for q in attempt.questions:
            q.correct_answer = ""
            q.explanation = ""
        # Return TestAttemptResponse (schema hides correct answer implicitly if not in model, or we just set it blank)
        return TestAttemptResponse.model_validate(attempt)
    else:
        return TestResultResponse.model_validate(attempt)

@router.post("/{attempt_id}/save-answer")
def save_single_answer(
    attempt_id: int, 
    answer: AnswerSubmission,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    attempt = get_test_attempt(db, attempt_id, current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Test attempt not found")
    if attempt.status != 'in_progress':
        raise HTTPException(status_code=400, detail="Test already completed")
        
    ans = save_answer(db, attempt_id, answer)
    return {"message": "Answer saved successfully"}

@router.post("/{attempt_id}/submit", response_model=TestResultResponse)
def submit_mock_test(
    attempt_id: int, 
    submission: SubmitTestRequest,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    attempt = get_test_attempt(db, attempt_id, current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Test attempt not found")
    if attempt.status != 'in_progress':
        raise HTTPException(status_code=400, detail="Test already completed")
        
    completed_attempt = submit_test(db, attempt_id, submission.answers)
    return completed_attempt
