from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.issue import router as issue_router
from app.database.base_class import Base
from app.database.session import engine

app = FastAPI(
    title="Issues & Insights Tracker",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(issue_router, prefix="/issue", tags=["issue"])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)