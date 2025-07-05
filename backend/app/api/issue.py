from typing import List, Optional

from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.attachment import AttachmentRead
from app.crud.issue import IssueRepository
from app.crud.attachment import AttachmentRepository
from app.schemas.issues import IssueCreate, IssueRead, IssueUpdate, SeverityEnum
from app.dependencies.auth import get_db, get_current_user, require_role
from app.models.user import RoleEnum, User
from app.utils.storage import save_upload_file
from app.utils import pubsub_instance  

router = APIRouter(tags=["issues"])

def get_issue_repo(db: Session = Depends(get_db)) -> IssueRepository:
    return IssueRepository(db)

def get_attach_repo(db: Session = Depends(get_db)) -> AttachmentRepository:
    return AttachmentRepository(db)

@router.post("/create", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
async def create_issue(
    title: str = Form(...),
    description: str = Form(...),
    severity: SeverityEnum = Form(SeverityEnum.LOW),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_role(RoleEnum.REPORTER, RoleEnum.ADMIN)),
    repo: IssueRepository = Depends(get_issue_repo),
    attach_repo: AttachmentRepository = Depends(get_attach_repo),
):
    issue_in = IssueCreate(title=title, description=description, severity=severity)
    issue = repo.create(issue_in, reporter_id=current_user.id)

    attachment = None
    if file:
        path = save_upload_file(file)
        attachment = attach_repo.create_issue_with_attachment(issue.id, file.filename, path)
        repo.db.refresh(issue)

    issue_data = IssueRead.model_validate(issue)
    if attachment:
        issue_data.attachment = AttachmentRead.model_validate(attachment)

    return issue_data


@router.get("/getall", response_model=List[IssueRead])
def list_issues(
    current_user: User = Depends(get_current_user),
    repo: IssueRepository = Depends(get_issue_repo),
    attach_repo: AttachmentRepository = Depends(get_attach_repo),
):
    if current_user.role == RoleEnum.REPORTER:
        issues = repo.list_by_reporter(current_user.id)
    else:
        issues = repo.list_all()

    results = []
    for issue in issues:
        attachment = attach_repo.get_by_issue_id(issue.id)
        issue_data = IssueRead.model_validate(issue)
        if attachment:
            issue_data.attachment = AttachmentRead.model_validate(attachment)
        results.append(issue_data)

    return results

@router.get("/{issue_id}", response_model=IssueRead)
def get_issue(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    repo: IssueRepository = Depends(get_issue_repo),
    attach_repo: AttachmentRepository = Depends(get_attach_repo),
):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if current_user.role == RoleEnum.REPORTER and issue.reporter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted to view this issue")

    attachment = attach_repo.get_by_issue_id(issue_id)
    return IssueRead.model_validate(issue, update={"attachment": attachment})





@router.patch(
    "/{issue_id}/status",
    response_model=IssueRead
)
async def update_issue_status(
    issue_id: int,
    update_in: IssueUpdate,
    current_user: User = Depends(require_role(RoleEnum.MAINTAINER, RoleEnum.ADMIN)),
    repo: IssueRepository = Depends(get_issue_repo),
):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    updated_issue = repo.update_status(issue, update_in.status)

    await pubsub_instance.publish({
        "type": "issue_updated",
        "issue": IssueRead.from_orm(updated_issue).model_dump(),
    })

    return updated_issue

@router.put(
    "/{issue_id}",
    response_model=IssueRead
)
def update_issue_details(
    issue_id: int,
    issue_in: IssueCreate,
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.REPORTER)),
    repo: IssueRepository = Depends(get_issue_repo),
):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue.title = issue_in.title
    issue.description = issue_in.description
    issue.severity = issue_in.severity
    repo.db.commit()
    repo.db.refresh(issue)
    return issue

@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_issue(
    issue_id: int,
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.REPORTER)),

    repo: IssueRepository = Depends(get_issue_repo),
):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    repo.db.delete(issue)
    repo.db.commit()
    await pubsub_instance.publish({
        "type": "issue_deleted",
        "issue_id": issue_id,
    })
