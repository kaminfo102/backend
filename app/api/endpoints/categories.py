from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import category as models
from ...schemas import category as schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Category)
    
    if search:
        query = query.filter(models.Category.title.ilike(f"%{search}%"))
    
    total = query.count()
    categories = query.offset(skip).limit(limit).all()
    
    return {
        "items": categories,
        "total": total,
        "has_more": total > skip + limit
    }

@router.get("/{category_id}/exams", response_model=List[schemas.ExamInCategory])
def get_category_exams(
    category_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    exams = db.query(models.Exam).filter(
        models.Exam.category_id == category_id
    ).offset(skip).limit(limit).all()
    
    return exams
