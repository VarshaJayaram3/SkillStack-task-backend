from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    resource_type = Column(String)
    platform = Column(String)
    status = Column(String)
    goal_hours = Column(Float, default=0)
    spent_hours = Column(Float, default=0)
    difficulty = Column(Integer)
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))

    notes = relationship("Note", back_populates="skill", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))

    skill_id = Column(Integer, ForeignKey("skills.id"))
    skill = relationship("Skill", back_populates="notes")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # resource_type | platform
    value = Column(String, unique=True)

class HourLog(Base):
    __tablename__ = "hour_logs"

    id = Column(Integer, primary_key=True, index=True)
    hours = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    skill_id = Column(Integer, ForeignKey("skills.id"))