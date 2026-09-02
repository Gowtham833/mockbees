from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .question import QuestionResponse, QuestionWithAnswer
from .exam import ExamResponse

class TestConfigRequest(BaseModel):
    exam_id: int
    num_questions: Optional[int] = None

class UserAnswerResponse(BaseModel):
    id: int
    question_id: int
    selected_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    time_spent_seconds: int
    is_marked_for_review: bool
    
    model_config = ConfigDict(from_attributes=True)

class TestAttemptResponse(BaseModel):
    id: int
    user_id: int
    exam_id: int
    status: str
    total_questions: int
    duration_minutes: int
    duration_seconds: int
    started_at: datetime
    generation_status: str
    error_message: Optional[str] = None
    exam: Optional[ExamResponse] = None
    questions: List[QuestionResponse] = []
    user_answers: List[UserAnswerResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: Optional[str] = None
    time_spent_seconds: int = 0
    is_marked_for_review: bool = False

class SubmitTestRequest(BaseModel):
    answers: List[AnswerSubmission]

class TestResultResponse(BaseModel):
    id: int
    exam_id: int
    status: str
    total_questions: int
    duration_minutes: int
    duration_seconds: int
    correct_answers: int
    incorrect_answers: int
    unanswered: int
    score: float
    max_score: float
    accuracy: float
    time_taken_seconds: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    exam: Optional[ExamResponse] = None
    questions: List[QuestionWithAnswer] = []
    user_answers: List[UserAnswerResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
