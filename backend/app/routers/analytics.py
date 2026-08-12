from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.analytics import OverviewStats, TopicPerformance, SubjectPerformance, PerformanceHistory
from app.services.analytics_service import get_user_overview, get_performance_history, get_subject_performance, get_topic_performance, get_weak_areas

router = APIRouter()

@router.get("/overview", response_model=OverviewStats)
def read_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_overview(db, current_user.id)

@router.get("/topic-performance", response_model=List[TopicPerformance])
def read_topic_performance(
    exam_id: Optional[int] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # exam_id could be None, the service should handle it
    return get_topic_performance(db, current_user.id, exam_id or 0)

@router.get("/subject-performance", response_model=List[SubjectPerformance])
def read_subject_performance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_subject_performance(db, current_user.id)

@router.get("/history", response_model=List[PerformanceHistory])
def read_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_performance_history(db, current_user.id)

@router.get("/weak-areas")
def read_weak_areas(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_weak_areas(db, current_user.id)
