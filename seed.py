from app.database import SessionLocal, Base, engine
from app import models
import datetime

# Recreate DB tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create a college
college = models.College(name="ABC College")
db.add(college)
db.commit()
db.refresh(college)

# Create students
students = [
    models.Student(name="Alice", email="alice@example.com", college_id=college.id),
    models.Student(name="Bob", email="bob@example.com", college_id=college.id),
    models.Student(name="Charlie", email="charlie@example.com", college_id=college.id),
]
db.add_all(students)
db.commit()

# Create events
events = [
    models.Event(
        college_id=college.id,
        title="Python Workshop",
        type=models.EventType.workshop,
        starts_at=datetime.datetime(2025, 9, 10, 10, 0),
        ends_at=datetime.datetime(2025, 9, 10, 12, 0),
        location="Hall A",
    ),
    models.Event(
        college_id=college.id,
        title="AI Seminar",
        type=models.EventType.seminar,
        starts_at=datetime.datetime(2025, 9, 12, 14, 0),
        ends_at=datetime.datetime(2025, 9, 12, 16, 0),
        location="Hall B",
    ),
    models.Event(
        college_id=college.id,
        title="Hackathon",
        type=models.EventType.hackathon,
        starts_at=datetime.datetime(2025, 9, 15, 9, 0),
        ends_at=datetime.datetime(2025, 9, 16, 18, 0),
        location="Lab 1",
    ),
]
db.add_all(events)
db.commit()

print("✅ Seed data inserted: 1 college, 3 students, 3 events")
