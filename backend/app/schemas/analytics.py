from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OverviewStats(BaseModel):
    total_tests: int
    average_score: float
    average_accuracy: float
    best_score_percentage: float

class TopicPerformance(BaseModel):
    topic: str
    total_questions: int
    correct: int
    accuracy: float

class SubjectPerformance(BaseModel):
    subject: str
    total_questions: int
    correct: int
    accuracy: float
    topics: List[TopicPerformance]

class PerformanceHistory(BaseModel):
    attempt_id: int
    exam_name: str
    date: datetime
    score: float
    max_score: float
    accuracy: float
