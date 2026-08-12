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
    
    questions = generate_questions(exam.name, exam.subjects, num_q, negative_marks=exam.negative_marking)
    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate questions")
        
    attempt = create_test_attempt(db, current_user.id, exam.id, questions)
    
    # Hide correct answer and explanation for in-progress tests
    for q in attempt.questions:
        q.correct_answer = ""
        q.explanation = ""
        
    return attempt

@router.post("/generate-stream")
def generate_mock_test_stream(
    config: TestConfigRequest,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    exam = get_exam_by_id(db, config.exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
        
    num_q = config.num_questions or exam.total_questions
    
    def event_stream():
        progress_data = {"completed": 0, "total": 0, "current_subject": "", "status": "generating"}
        generation_result = {"questions": None, "error": None}
        
        def progress_callback(completed, total, subject_name):
            progress_data["completed"] = completed
            progress_data["total"] = total
            progress_data["current_subject"] = subject_name
        
        def generate_in_thread():
            try:
                questions = generate_questions(
                    exam.name, exam.subjects, num_q, 
                    negative_marks=exam.negative_marking,
                    progress_callback=progress_callback
                )
                generation_result["questions"] = questions
            except Exception as e:
                generation_result["error"] = str(e)
        
        thread = threading.Thread(target=generate_in_thread)
        thread.start()
        
        last_completed = -1
        while thread.is_alive():
            if progress_data["completed"] != last_completed:
                last_completed = progress_data["completed"]
                yield f"data: {json.dumps({'type': 'progress', 'completed': progress_data['completed'], 'total': progress_data['total'], 'subject': progress_data['current_subject']})}\n\n"
            time.sleep(0.5)
        
        thread.join()
        
        if generation_result["error"]:
            yield f"data: {json.dumps({'type': 'error', 'message': generation_result['error']})}\n\n"
            return
        
        questions = generation_result["questions"]
        if not questions:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to generate questions'})}\n\n"
            return
        
        attempt = create_test_attempt(db, current_user.id, exam.id, questions)
        
        # Hide correct answer and explanation for in-progress tests
        for q in attempt.questions:
            q.correct_answer = ""
            q.explanation = ""
        
        from app.schemas.test_attempt import TestAttemptResponse
        response_data = TestAttemptResponse.model_validate(attempt).model_dump(mode='json')
        yield f"data: {json.dumps({'type': 'complete', 'data': response_data})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

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
