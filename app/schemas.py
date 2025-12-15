from pydantic import BaseModel
from typing import List
from datetime import datetime


class NoteCreate(BaseModel):
    content: str


class NoteResponse(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SkillCreate(BaseModel):
    name: str
    resource_type: str
    platform: str
    status: str
    goal_hours: float
    spent_hours: float
    difficulty: int


class SkillUpdate(SkillCreate):
    pass


class SkillResponse(SkillCreate):
    id: int
    created_at: datetime
    notes: List[NoteResponse] = []

    class Config:
        orm_mode = True


class OptionCreate(BaseModel):
    type: str
    value: str


class OptionResponse(OptionCreate):
    id: int

    class Config:
        orm_mode = True
