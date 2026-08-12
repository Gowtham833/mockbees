from pydantic import BaseModel, ConfigDict
from typing import Optional

class QuestionResponse(BaseModel):
    id: int
    subject: str
    topic: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    marks: float
    negative_marks: float
    difficulty: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class QuestionWithAnswer(QuestionResponse):
    correct_answer: str
    explanation: Optional[str] = None
