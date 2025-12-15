from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()

# ---------------------------
# DB dependency
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# CREATE SKILL
# ---------------------------
@router.post("/", response_model=schemas.SkillResponse)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


# ---------------------------
# GET ALL SKILLS (WITH NOTES)
# ---------------------------
@router.get("/", response_model=list[schemas.SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()


# ---------------------------
# UPDATE SKILL (EDIT FORM)
# ---------------------------
@router.put("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(
    skill_id: int,
    skill: schemas.SkillUpdate,
    db: Session = Depends(get_db)
):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    for key, value in skill.dict().items():
        setattr(db_skill, key, value)

    db.commit()
    db.refresh(db_skill)
    return db_skill


# ---------------------------
# ADD HOURS TO SKILL
# ---------------------------
@router.post("/{skill_id}/add-hours", response_model=schemas.SkillResponse)
def add_hours(skill_id: int, hours: float, db: Session = Depends(get_db)):
    if hours <= 0:
        raise HTTPException(status_code=400, detail="Hours must be greater than 0")

    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # 1. Update spent hours
    db_skill.spent_hours += hours

    # ✅ 2. Auto move Started → In Progress (ONLY ONCE)
    if db_skill.status == "Started":
        db_skill.status = "In Progress"

    # 3. Create hour log
    hour_log = models.HourLog(
        hours=hours,
        skill_id=skill_id
    )
    db.add(hour_log)

    db.commit()
    db.refresh(db_skill)

    return db_skill


# ---------------------------
# ADD NOTE (HISTORY)
# ---------------------------
@router.post("/{skill_id}/add-note", response_model=schemas.NoteResponse)
def add_note(
    skill_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db)
):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db_note = models.Note(
        content=note.content,
        skill_id=skill_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# ---------------------------
# DELETE SKILL
# ---------------------------
@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(db_skill)
    db.commit()

    return {"message": "Skill deleted successfully"}
