from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    score = Column(Float)
    passed = Column(Boolean)
    time_taken = Column(Integer)  # in seconds
    answers = Column(JSON)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="test_results")
    exam = relationship("Exam", back_populates="results")
