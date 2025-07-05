# app/routes/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.issues import Issue
from app.dependencies.auth import get_current_user, get_db
from sqlalchemy import func
from app.models.user import RoleEnum


router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/issue_severity_counts")
def issue_severity_counts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Issue.severity, func.count(Issue.id)).filter(Issue.status == 'OPEN')

    if current_user.role == RoleEnum.REPORTER:
        query = query.filter(Issue.reporter_id == current_user.id)

    result = query.group_by(Issue.severity).all()

    return {severity: count for severity, count in result}
