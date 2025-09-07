from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/{event_id}")
def mark_attendance(event_id: int, att: schemas.AttendanceIn, db: Session = Depends(database.get_db)):
    attendance = models.Attendance(event_id=event_id, student_id=att.student_id, present=att.present)
    db.add(attendance)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Attendance already marked")
    db.refresh(attendance)
    return attendance
