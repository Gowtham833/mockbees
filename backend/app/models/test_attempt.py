from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    status = Column(String, nullable=False) # 'in_progress', 'completed', 'abandoned'
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    unanswered = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    max_score = Column(Float, nullable=False)
    accuracy = Column(Float, default=0.0)
    time_taken_seconds = Column(Integer, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    generation_status = Column(String, default="READY") # 'PENDING', 'GENERATING', 'READY', 'FAILED'
    error_message = Column(String, nullable=True)

    user = relationship("User")
    exam = relationship("Exam", back_populates="test_attempts")

    @property
    def duration_seconds(self):
        if self.exam and self.exam.duration_minutes:
            return int(self.exam.duration_minutes * 60 * (self.total_questions / max(self.exam.total_questions, 1)))
        return 0

    @property
    def duration_minutes(self):
        seconds = self.duration_seconds
        return int((seconds + 59) // 60) if seconds else 0
    questions = relationship("Question", back_populates="test_attempt", foreign_keys="[Question.test_attempt_id]")
    user_answers = relationship("UserAnswer", back_populates="test_attempt")

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_attempt_id = Column(Integer, ForeignKey("test_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    is_marked_for_review = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    test_attempt = relationship("TestAttempt", back_populates="user_answers")
    question = relationship("Question")
