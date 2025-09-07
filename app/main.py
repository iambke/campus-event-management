from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from .routers import events, registrations, attendance, feedback, reports
from .database import Base, engine, get_db
from . import models

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Events Management")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(registrations.router, prefix="/registrations", tags=["Registrations"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---- Frontend routes ---- #

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    events_data = [
        {
            "id": e.id,
            "title": e.title,
            "type": e.type.value if hasattr(e.type, "value") else e.type,
            "location": e.location or "",
        }
        for e in events
    ]
    return templates.TemplateResponse("events.html", {"request": request, "events": events_data})


@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
