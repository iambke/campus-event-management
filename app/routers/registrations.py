from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/{event_id}")
def register(event_id: int, reg: schemas.RegistrationIn, db: Session = Depends(database.get_db)):
    registration = models.Registration(event_id=event_id, student_id=reg.student_id)
    db.add(registration)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already registered")
    db.refresh(registration)
    return registration
