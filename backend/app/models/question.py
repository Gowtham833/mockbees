from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    test_attempt_id = Column(Integer, ForeignKey("test_attempts.id"), nullable=True)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String, nullable=False)
    marks = Column(Float, default=1.0)
    negative_marks = Column(Float, default=0.25)
    created_at = Column(DateTime, server_default=func.now())

    exam = relationship("Exam", back_populates="questions")
    test_attempt = relationship("TestAttempt", back_populates="questions", foreign_keys=[test_attempt_id])
