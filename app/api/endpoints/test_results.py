from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import test_result as models
from ...schemas import test_result as schemas
from ...auth.jwt import get_current_user

router = APIRouter()

@router.post("/submit", response_model=schemas.TestResultResponse)
def submit_test(
    result: schemas.TestResultCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate score and check if passed
    exam = db.query(models.Exam).filter(models.Exam.id == result.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    correct_answers = 0
    total_questions = len(result.answers)
    
    for answer in result.answers:
        question = db.query(models.Question).filter(
            models.Question.id == answer.question_id
        ).first()
        if question and question.correct_answer == answer.selected_option:
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    passed = score >= exam.passing_score
    
    # Create test result
    test_result = models.TestResult(
        user_id=current_user.id,
        exam_id=result.exam_id,
        score=score,
        passed=passed,
        time_taken=result.time_taken,
        answers=result.answers
    )
    db.add(test_result)
    
    # Update user stats
    stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == current_user.id
    ).first()
    
    if stats:
        stats.total_tests += 1
        stats.average_score = (stats.average_score * (stats.total_tests - 1) + score) / stats.total_tests
        # اصلاح محاسبه pass_rate
        if stats.total_tests > 1 :
             stats.pass_rate = ((stats.pass_rate * (stats.total_tests - 1)) + (1 if passed else 0)) / stats.total_tests
        else :
             stats.pass_rate = (1 if passed else 0)

        stats.total_time += result.time_taken
    else:
        new_stats = models.UserStats(
            user_id=current_user.id,
            total_tests=1,
            average_score = score,
            pass_rate = (1 if passed else 0),
            total_time=result.time_taken
        )
        db.add(new_stats)

    db.commit()
    db.refresh(test_result)
    return test_result
