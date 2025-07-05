from sqlalchemy.orm import Session
from app.models.issues import Issue, StatusEnum, SeverityEnum
from app.schemas.issues import IssueCreate

class IssueRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, issue_in: IssueCreate, reporter_id: int) -> Issue:
        issue = Issue(**issue_in.model_dump(), reporter_id=reporter_id)
        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def get(self, issue_id: int) -> Issue | None:
        return self.db.query(Issue).filter(Issue.id == issue_id).first()

    def list_all(self) -> list[Issue]:
        return self.db.query(Issue).order_by(Issue.created_at.desc()).all()

    def list_by_reporter(self, reporter_id: int) -> list[Issue]:
        return (
            self.db.query(Issue)
            .filter(Issue.reporter_id == reporter_id)
            .order_by(Issue.created_at.desc())
            .all()
        )

    def update_status(self, issue: Issue, new_status: StatusEnum, new_severity: SeverityEnum) -> Issue:
        issue.status = new_status
        issue.severity = new_severity
        self.db.commit()
        self.db.refresh(issue)
        return issue
