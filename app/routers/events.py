from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/")
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/")
def list_events(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()
