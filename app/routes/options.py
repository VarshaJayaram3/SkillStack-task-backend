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
# ADD OPTION (Resource / Platform)
# ---------------------------
@router.post("/", response_model=schemas.OptionResponse)
def add_option(option: schemas.OptionCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Option).filter(
        models.Option.type == option.type,
        models.Option.value == option.value
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Option already exists")

    db_option = models.Option(**option.dict())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


# ---------------------------
# GET ALL OPTIONS
# ---------------------------
@router.get("/", response_model=list[schemas.OptionResponse])
def get_options(db: Session = Depends(get_db)):
    return db.query(models.Option).all()


# ---------------------------
# DELETE OPTION
# ---------------------------
@router.delete("/{option_id}")
def delete_option(option_id: int, db: Session = Depends(get_db)):
    option = db.query(models.Option).filter(models.Option.id == option_id).first()

    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    db.delete(option)
    db.commit()

    return {"message": "Option deleted successfully"}
