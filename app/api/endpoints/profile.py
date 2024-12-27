from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import user_stats as stats_model
from ...models import test_result as result_model
from ...schemas import profile as schemas
from ...auth.jwt import get_current_user

router = APIRouter()

@router.get("/stats", response_model=schemas.UserStats)
def get_user_stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = db.query(stats_model.UserStats).filter(
        stats_model.UserStats.user_id == current_user.id
    ).first()
    
    if not stats:
        stats = stats_model.UserStats(user_id=current_user.id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats

@router.get("/test-history", response_model=List[schemas.TestResult])
def get_test_history(
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = db.query(stats_model.TestResult).filter(
        result_model.TestResult.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return results
