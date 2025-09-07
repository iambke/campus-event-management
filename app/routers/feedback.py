from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/{event_id}")
def give_feedback(event_id: int, fb: schemas.FeedbackIn, db: Session = Depends(database.get_db)):
    feedback = models.Feedback(event_id=event_id, student_id=fb.student_id, rating=fb.rating, comment=fb.comment)
    db.add(feedback)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Feedback already given or invalid rating")
    db.refresh(feedback)
    return feedback

@router.get("/{event_id}/list")
def list_feedback(event_id: int, db: Session = Depends(database.get_db)):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.event_id == event_id).all()
    return feedbacks
