from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from datetime import datetime

class SubjectInfo(BaseModel):
    name: str
    weightage: int
    topics: List[str]

class ExamResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str] = None
    total_questions: int
    total_marks: int
    duration_minutes: int
    negative_marking: float
    subjects: List[SubjectInfo]
    instructions: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ExamCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    is_active: bool
    created_at: datetime
    exams: Optional[List[ExamResponse]] = None
    
    model_config = ConfigDict(from_attributes=True)

class ExamListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    total_questions: int
    total_marks: int
    duration_minutes: int
    
    model_config = ConfigDict(from_attributes=True)
