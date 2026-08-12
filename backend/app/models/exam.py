from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

class ExamCategory(Base):
    __tablename__ = "exam_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    exams = relationship("Exam", back_populates="category")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("exam_categories.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    total_questions = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    negative_marking = Column(Float, default=0.25)
    subjects = Column(JSON, nullable=False)
    instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    category = relationship("ExamCategory", back_populates="exams")
    questions = relationship("Question", back_populates="exam")
    test_attempts = relationship("TestAttempt", back_populates="exam")
