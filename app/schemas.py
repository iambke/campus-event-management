from pydantic import BaseModel
from typing import Optional
import datetime

class EventCreate(BaseModel):
    college_id: int
    title: str
    type: str
    starts_at: Optional[datetime.datetime] = None
    ends_at: Optional[datetime.datetime] = None
    location: Optional[str] = None

class EventOut(BaseModel):
    id: int
    title: str
    type: str
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    location: str
    class Config:
        orm_mode = True

class RegistrationIn(BaseModel):
    student_id: int

class AttendanceIn(BaseModel):
    student_id: int
    present: bool

class FeedbackIn(BaseModel):
    student_id: int
    rating: int
    comment: Optional[str] = None
