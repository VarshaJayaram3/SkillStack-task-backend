from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Skill, HourLog
from datetime import date

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard_summary(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    hour_logs = db.query(HourLog).all()

    today = date.today()

    total_hours = sum(log.hours for log in hour_logs)
    today_hours = sum(
        log.hours for log in hour_logs
        if log.created_at.date() == today
    )

    return {
        "total_skills": len(skills),
        "completed": len([s for s in skills if s.status == "Completed"]),
        "in_progress": len([s for s in skills if s.status == "In Progress"]),
        "total_hours": total_hours,
        "today_hours": today_hours
    }

@router.get("/platform-breakdown")
def platform_breakdown(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    result = {}

    for skill in skills:
        if skill.platform:
            result[skill.platform] = result.get(skill.platform, 0) + 1

    return [{"label": k, "value": v} for k, v in result.items()]

@router.get("/resource-breakdown")
def resource_breakdown(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    result = {}

    for skill in skills:
        if skill.resource_type:
            result[skill.resource_type] = result.get(skill.resource_type, 0) + 1

    return [{"label": k, "value": v} for k, v in result.items()]
