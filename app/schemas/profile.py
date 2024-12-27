from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# User Stats Schema
class UserStatsBase(BaseModel):
    user_id: int
    total_tests: Optional[int] = 0
    average_score: Optional[float] = 0.0
    tests_completed: Optional[int] = 0

class UserStats(UserStatsBase):
    id: int
    class Config:
        orm_mode = True

# Test Result Schema
class TestResultBase(BaseModel):
    user_id: int
    test_id: int
    score: int
    completed_at: Optional[datetime] = None


class TestResult(TestResultBase):
    id: int
    class Config:
        orm_mode = True
