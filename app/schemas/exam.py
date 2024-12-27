from pydantic import BaseModel
from typing import List, Optional

class QuestionOptionBase(BaseModel):
    text: str

class QuestionBase(BaseModel):
    text: str
    options: List[QuestionOptionBase]
    correct_answer: str

class ExamBase(BaseModel):
    title: str
    description: str
    duration: int
    category_id: int
    difficulty: str
    is_free: bool = True
    passing_score: float

class ExamCreate(ExamBase):
    questions: List[QuestionBase]

class ExamResponse(ExamBase):
    id: int
    questions: List[QuestionBase]

    class Config:
        from_attributes = True
