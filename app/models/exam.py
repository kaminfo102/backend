from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    duration = Column(Integer)  # in minutes
    category_id = Column(Integer, ForeignKey("categories.id"))
    difficulty = Column(String)  # easy, medium, hard
    is_free = Column(Boolean, default=True)
    passing_score = Column(Float)
    
    category = relationship("Category", back_populates="exams")
    questions = relationship("Question", back_populates="exam")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    text = Column(Text)
    correct_answer = Column(String)
    
    exam = relationship("Exam", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")

class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(Text)
    
    question = relationship("Question", back_populates="options")
