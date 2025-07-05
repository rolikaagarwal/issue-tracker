from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.issue import router as issues_router
from app.api.users import router as users_router  
from fastapi.staticfiles import StaticFiles
from app.database.base_class import Base
from app.database.session import engine, SessionLocal
from app.crud.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import RoleEnum
from app.core.config import settings
from app.api.events import router as  events_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.aggregator import aggregate_issue_counts
from datetime import datetime
from app.api.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.google_auth import router as google_router

app = FastAPI(
    title="Issues & Insights Tracker",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    repo = UserRepository(db)
    if not repo.get_by_email(settings.ADMIN_EMAIL):
        repo.create(
            UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD
            ),
            role=RoleEnum.ADMIN
        )
    db.close()

    scheduler.add_job(
        aggregate_issue_counts,
        trigger="interval",
        minutes=30,
        next_run_time=datetime.now()
    )
    scheduler.start()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(issues_router, prefix="/issues", tags=["issues"])
app.include_router(users_router, prefix="/users", tags=["admin"])
app.include_router(events_router, tags=["events"])
app.include_router(dashboard_router, tags=["dashboard"])
app.include_router(google_router, tags=["google"])

