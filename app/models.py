from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import enum
import datetime

class EventType(str, enum.Enum):
    workshop = "Workshop"
    seminar = "Seminar"
    fest = "Fest"
    talk = "Talk"
    hackathon = "Hackathon"

class EventStatus(str, enum.Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship("Student", back_populates="college")
    events = relationship("Event", back_populates="college")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    college = relationship("College", back_populates="students")
    registrations = relationship("Registration", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")
    feedback = relationship("Feedback", back_populates="student")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    title = Column(String, nullable=False)
    type = Column(Enum(EventType), nullable=False)
    starts_at = Column(DateTime, default=datetime.datetime.utcnow)
    ends_at = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(String)
    status = Column(Enum(EventStatus), default=EventStatus.scheduled)

    college = relationship("College", back_populates="events")
    registrations = relationship("Registration", back_populates="event")
    attendance = relationship("Attendance", back_populates="event")
    feedback = relationship("Feedback", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint("event_id", "student_id", name="unique_registration"),)

    event = relationship("Event", back_populates="registrations")
    student = relationship("Student", back_populates="registrations")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    present = Column(Boolean, default=False)
    check_in_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint("event_id", "student_id", name="unique_attendance"),)

    event = relationship("Event", back_populates="attendance")
    student = relationship("Student", back_populates="attendance")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("event_id", "student_id", name="unique_feedback"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )

    event = relationship("Event", back_populates="feedback")
    student = relationship("Student", back_populates="feedback")
