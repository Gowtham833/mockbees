from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.exam import ExamCategoryResponse, ExamResponse
from app.services.exam_service import get_categories, get_exams_by_category, get_exam_by_id

router = APIRouter()

@router.get("/categories", response_model=List[ExamCategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    categories = get_categories(db)
    for cat in categories:
        cat.exams = get_exams_by_category(db, cat.id)
    return categories

@router.get("/categories/{category_id}", response_model=ExamCategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    from app.models.exam import ExamCategory
    category = db.query(ExamCategory).filter(ExamCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.exams = get_exams_by_category(db, category_id)
    return category

@router.get("/{exam_id}", response_model=ExamResponse)
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = get_exam_by_id(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
