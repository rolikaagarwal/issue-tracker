import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.issues import Issue, SeverityEnum, StatusEnum
from app.models.user import User, RoleEnum


os.environ["ENV"] = "test"

def create_user(db: Session, email: str, role: RoleEnum) -> User:
    user = User(email=email, role=role, hashed_password="hashed_dummy")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_issue(db: Session, reporter_id: int, title="Test Issue", severity=SeverityEnum.LOW) -> Issue:
    issue = Issue(
        title=title,
        description="This is a test issue",
        severity=severity,
        status=StatusEnum.OPEN,
        reporter_id=reporter_id
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue

def test_create_issue(client: TestClient, db_session: Session):
    reporter = create_user(db_session, "reporter@example.com", RoleEnum.REPORTER)
    response = client.post(
        "/issues/create",
        data={
            "title": "New Issue",
            "description": "Issue description",
            "severity": "HIGH"
        },
        headers={"Authorization": f"Bearer {reporter.id}"}  # Simplified for test
    )
    assert response.status_code == 201
    assert response.json()["title"] == "New Issue"

def test_list_issues_as_reporter(client: TestClient, db_session: Session):
    reporter = create_user(db_session, "reporter2@example.com", RoleEnum.REPORTER)
    create_issue(db_session, reporter.id, title="R1")
    create_issue(db_session, reporter.id, title="R2")
    response = client.get("/issues/getall", headers={"Authorization": f"Bearer {reporter.id}"})
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_issue_by_id(client: TestClient, db_session: Session):
    reporter = create_user(db_session, "reporter3@example.com", RoleEnum.REPORTER)
    issue = create_issue(db_session, reporter.id, title="SingleIssue")
    response = client.get(f"/issues/{issue.id}", headers={"Authorization": f"Bearer {reporter.id}"})
    assert response.status_code == 200
    assert response.json()["title"] == "SingleIssue"

def test_update_issue_status(client: TestClient, db_session: Session):
    admin = create_user(db_session, "admin@example.com", RoleEnum.ADMIN)
    reporter = create_user(db_session, "reporter4@example.com", RoleEnum.REPORTER)
    issue = create_issue(db_session, reporter.id)
    response = client.patch(
        f"/issues/{issue.id}/status",
        json={"status": "DONE", "severity": "MEDIUM"},
        headers={"Authorization": f"Bearer {admin.id}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "DONE"

def test_update_issue_details(client: TestClient, db_session: Session):
    reporter = create_user(db_session, "reporter5@example.com", RoleEnum.REPORTER)
    issue = create_issue(db_session, reporter.id)
    response = client.put(
        f"/issues/{issue.id}",
        json={"title": "Updated Title", "description": "Updated", "severity": "HIGH"},
        headers={"Authorization": f"Bearer {reporter.id}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_issue(client: TestClient, db_session: Session):
    reporter = create_user(db_session, "reporter6@example.com", RoleEnum.REPORTER)
    issue = create_issue(db_session, reporter.id)
    response = client.delete(f"/issues/{issue.id}", headers={"Authorization": f"Bearer {reporter.id}"})
    assert response.status_code == 204
