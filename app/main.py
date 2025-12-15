from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import skills, options, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillStack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills.router, prefix="/skills", tags=["Skills"])
app.include_router(options.router, prefix="/options", tags=["Options"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
