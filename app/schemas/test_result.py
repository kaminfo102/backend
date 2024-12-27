from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnswerSchema(BaseModel):
    question_id: int
    selected_option: str

class TestResultBase(BaseModel):
    exam_id: int
    time_taken: int
    answers: List[AnswerSchema]

class TestResultCreate(TestResultBase):
    pass

class TestResult(TestResultBase):
    id: int
    user_id: int
    score: float
    passed: bool
    completed_at: datetime

    class Config:
        orm_mode = True


class TestResultResponse(TestResult):
    pass
