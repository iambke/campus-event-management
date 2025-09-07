from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, database

router = APIRouter()


# --- Existing reports --- #

@router.get("/events/popularity")
def event_popularity(db: Session = Depends(database.get_db)):
    results = (
        db.query(
            models.Event.title.label("title"),
            func.count(models.Registration.id).label("registrations")
        )
        .join(models.Registration, models.Event.id == models.Registration.event_id, isouter=True)
        .filter(models.Event.status != models.EventStatus.cancelled)   # exclude cancelled
        .group_by(models.Event.id)
        .order_by(func.count(models.Registration.id).desc())
        .all()
    )
    return [dict(r._mapping) for r in results]


@router.get("/students/participation")
def student_participation(db: Session = Depends(database.get_db)):
    results = (
        db.query(
            models.Student.name.label("name"),
            func.count(models.Attendance.event_id).label("events_attended")
        )
        .join(models.Attendance, models.Student.id == models.Attendance.student_id)
        .filter(models.Attendance.present == True)
        .group_by(models.Student.id)
        .order_by(func.count(models.Attendance.event_id).desc())
        .all()
    )
    return [dict(r._mapping) for r in results]


# --- New reports to meet assignment requirements --- #

@router.get("/events/{event_id}/summary")
def event_summary(event_id: int, db: Session = Depends(database.get_db)):
    """Summary of registrations, attendance %, and avg feedback per event"""
    total_regs = db.query(func.count(models.Registration.id)) \
                   .filter(models.Registration.event_id == event_id).scalar()
    present_count = db.query(func.count(models.Attendance.id)) \
                      .filter(models.Attendance.event_id == event_id,
                              models.Attendance.present == True).scalar()
    avg_rating = db.query(func.avg(models.Feedback.rating)) \
                   .filter(models.Feedback.event_id == event_id).scalar()

    attendance_pct = round((present_count / total_regs) * 100, 2) if total_regs else 0

    return {
        "event_id": event_id,
        "registrations": total_regs,
        "attendance_pct": attendance_pct,
        "avg_rating": round(avg_rating, 2) if avg_rating else None
    }


@router.get("/students/top")
def top_students(limit: int = 3, db: Session = Depends(database.get_db)):
    """Top N most active students based on attendance"""
    results = (
        db.query(
            models.Student.name.label("name"),
            func.count(models.Attendance.event_id).label("events_attended")
        )
        .join(models.Attendance, models.Student.id == models.Attendance.student_id)
        .filter(models.Attendance.present == True)
        .group_by(models.Student.id)
        .order_by(func.count(models.Attendance.event_id).desc())
        .limit(limit)
        .all()
    )
    return [dict(r._mapping) for r in results]


@router.get("/events/by_type/{event_type}")
def events_by_type(event_type: str, db: Session = Depends(database.get_db)):
    """Filter events by type (Workshop, Fest, Seminar, etc.)"""
    results = (
        db.query(models.Event)
        .filter(models.Event.type == event_type,
                models.Event.status != models.EventStatus.cancelled)
        .all()
    )
    return results
