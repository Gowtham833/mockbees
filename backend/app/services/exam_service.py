from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.models.exam import ExamCategory, Exam
from app.models.test_attempt import TestAttempt, UserAnswer
from app.schemas.test_attempt import AnswerSubmission
from app.models.question import Question

def get_categories(db: Session):
    return db.query(ExamCategory).all()

def get_exams_by_category(db: Session, category_id: int):
    return db.query(Exam).filter(Exam.category_id == category_id).all()

def get_exam_by_id(db: Session, exam_id: int):
    return db.query(Exam).filter(Exam.id == exam_id).first()


def create_test_attempt(db: Session, user_id: int, exam_id: int, num_questions: int):
    exam = get_exam_by_id(db, exam_id)
    
    attempt = TestAttempt(
        user_id=user_id,
        exam_id=exam_id,
        status='in_progress',
        generation_status='PENDING',
        total_questions=num_questions,
        # max_score will be updated dynamically or calculated based on num_questions
        max_score=exam.total_marks * (num_questions / exam.total_questions) if exam.total_questions > 0 else 0.0
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return attempt

def get_test_attempt(db: Session, attempt_id: int, user_id: int):
    return db.query(TestAttempt).filter(
        TestAttempt.id == attempt_id, TestAttempt.user_id == user_id
    ).first()

def save_answer(db: Session, attempt_id: int, answer_data: AnswerSubmission):
    ans = db.query(UserAnswer).filter(
        UserAnswer.test_attempt_id == attempt_id,
        UserAnswer.question_id == answer_data.question_id
    ).first()
    
    if not ans:
        ans = UserAnswer(
            test_attempt_id=attempt_id,
            question_id=answer_data.question_id
        )
        db.add(ans)
        
    ans.selected_answer = answer_data.selected_answer
    ans.time_spent_seconds = answer_data.time_spent_seconds
    ans.is_marked_for_review = answer_data.is_marked_for_review
    
    db.commit()
    return ans

def submit_test(db: Session, attempt_id: int, answers_data: List[AnswerSubmission]):
    attempt = db.query(TestAttempt).filter(TestAttempt.id == attempt_id).first()
    if not attempt or attempt.status == 'completed':
        return attempt
        
    for data in answers_data:
        save_answer(db, attempt_id, data)
        
    calculate_score(db, attempt_id)
    attempt.status = 'completed'
    attempt.completed_at = datetime.utcnow()
    
    # Calculate time taken
    if attempt.started_at and attempt.completed_at:
        attempt.time_taken_seconds = int((attempt.completed_at - attempt.started_at).total_seconds())
        
    db.commit()
    db.refresh(attempt)
    return attempt

def calculate_score(db: Session, attempt_id: int):
    attempt = db.query(TestAttempt).filter(TestAttempt.id == attempt_id).first()
    questions = db.query(Question).filter(Question.test_attempt_id == attempt_id).all()
    user_answers = db.query(UserAnswer).filter(UserAnswer.test_attempt_id == attempt_id).all()
    
    ans_map = {ans.question_id: ans for ans in user_answers}
    
    correct = 0
    incorrect = 0
    unanswered = 0
    score = 0.0
    
    for q in questions:
        ans = ans_map.get(q.id)
        if not ans or not ans.selected_answer:
            unanswered += 1
        elif ans.selected_answer == q.correct_answer:
            correct += 1
            score += q.marks
            ans.is_correct = True
        else:
            incorrect += 1
            score -= q.negative_marks
            ans.is_correct = False
            
    attempt.correct_answers = correct
    attempt.incorrect_answers = incorrect
    attempt.unanswered = unanswered
    attempt.score = score
    total_answered = correct + incorrect
    attempt.accuracy = (correct / total_answered * 100) if total_answered > 0 else 0.0
    db.commit()
