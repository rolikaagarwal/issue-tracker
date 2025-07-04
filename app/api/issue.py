from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.issue import IssueRepository
from app.schemas.issues import IssueCreate, IssueRead, IssueUpdate
from app.dependencies.auth import get_db, get_current_user, require_role
from app.schemas.user import UserRead
from app.models.user import RoleEnum

router = APIRouter()

def get_issue_repo(db: Session = Depends(get_db)) -> IssueRepository:
    return IssueRepository(db)

@router.post("/", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
def create_issue(
    issue_in: IssueCreate,
    current_user: UserRead = Depends(require_role(RoleEnum.REPORTER)),
    repo: IssueRepository = Depends(get_issue_repo),
):
    return repo.create(issue_in, reporter_id=current_user.id)

@router.get("/", response_model=list[IssueRead])
def list_issues(
    current_user: UserRead = Depends(get_current_user),
    repo: IssueRepository = Depends(get_issue_repo),
):
    if current_user.role == RoleEnum.REPORTER:
        return repo.list_by_reporter(current_user.id)
    return repo.list_all()

@router.patch("/{issue_id}/status", response_model=IssueRead)
def update_issue_status(
    issue_id: int,
    update_in: IssueUpdate,
    current_user: UserRead = Depends(require_role(RoleEnum.MAINTAINER)),
    repo: IssueRepository = Depends(get_issue_repo),
):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return repo.update_status(issue, update_in.status)
