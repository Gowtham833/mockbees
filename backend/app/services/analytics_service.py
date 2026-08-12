from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.test_attempt import TestAttempt, UserAnswer
from app.models.question import Question

def get_user_overview(db: Session, user_id: int):
    attempts = db.query(TestAttempt).filter(TestAttempt.user_id == user_id, TestAttempt.status == 'completed').all()
    if not attempts:
        return {
            "total_tests": 0,
            "average_score": 0.0,
            "average_accuracy": 0.0,
            "best_score_percentage": 0.0
        }
        
    total_tests = len(attempts)
    avg_score = sum(a.score for a in attempts) / total_tests
    avg_acc = sum(a.accuracy for a in attempts) / total_tests
    best_perc = max((a.score / a.max_score * 100) if a.max_score else 0 for a in attempts)
    
    return {
        "total_tests": total_tests,
        "average_score": avg_score,
        "average_accuracy": avg_acc,
        "best_score_percentage": best_perc
    }

def get_performance_history(db: Session, user_id: int):
    attempts = db.query(TestAttempt).filter(
        TestAttempt.user_id == user_id, 
        TestAttempt.status == 'completed'
    ).order_by(TestAttempt.completed_at.asc()).all()
    
    result = []
    for a in attempts:
        result.append({
            "attempt_id": a.id,
            "exam_name": a.exam.name if a.exam else "Unknown",
            "date": a.completed_at,
            "score": a.score,
            "max_score": a.max_score,
            "accuracy": a.accuracy
        })
    return result

def get_subject_performance(db: Session, user_id: int):
    # For simplicity, returning empty for now
    return []

def get_topic_performance(db: Session, user_id: int, exam_id: int):
    # For simplicity, returning empty for now
    return []

def get_weak_areas(db: Session, user_id: int):
    return []
