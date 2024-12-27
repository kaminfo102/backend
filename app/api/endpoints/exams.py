from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import exam as models
from ...schemas import exam as schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ExamResponse])
def get_exams(
    skip: int = 0,
    limit: int = 10,
    category_id: int = None,
    difficulty: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Exam)
    
    if category_id:
        query = query.filter(models.Exam.category_id == category_id)
    if difficulty:
        query = query.filter(models.Exam.difficulty == difficulty)
    
    exams = query.offset(skip).limit(limit).all()
    return exams

@router.get("/{exam_id}", response_model=schemas.ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.post("/", response_model=schemas.ExamResponse)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    db_exam = models.Exam(
        title=exam.title,
        description=exam.description,
        duration=exam.duration,
        category_id=exam.category_id,
        difficulty=exam.difficulty,
        is_free=exam.is_free,
        passing_score=exam.passing_score
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    
    for question_data in exam.questions:
        question = models.Question(
            exam_id=db_exam.id,
            text=question_data.text,
            correct_answer=question_data.correct_answer
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        for option_data in question_data.options:
            option = models.QuestionOption(
                question_id=question.id,
                text=option_data.text
            )
            db.add(option)
    
    db.commit()
    return db_exam
