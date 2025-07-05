from app.main import app
from app.dependencies.auth import get_current_user
from app.models.issues import Issue
from app.models.user import RoleEnum

def _dummy_user(user_id, role):
    class User:
        def __init__(self):
            self.id = user_id
            self.role = role
    return User()


def override_admin_user():
    return _dummy_user(user_id=1, role=RoleEnum.ADMIN)

def override_reporter_user():
    return _dummy_user(user_id=2, role=RoleEnum.REPORTER)


def test_issue_severity_counts_admin(client, db_session):
    issues = [
        Issue(title="A", description="x", severity="LOW", status="OPEN", reporter_id=2),
        Issue(title="B", description="y", severity="HIGH", status="OPEN", reporter_id=3),
        Issue(title="C", description="z", severity="LOW", status="CLOSED", reporter_id=2),
        Issue(title="D", description="w", severity="MEDIUM", status="OPEN", reporter_id=4),
    ]
    db_session.add_all(issues)
    db_session.commit()

    app.dependency_overrides[get_current_user] = override_admin_user
    response = client.get("/dashboard/issue_severity_counts")
    assert response.status_code == 200
    data = response.json()
    assert data == {"LOW": 1, "HIGH": 1, "MEDIUM": 1}
    app.dependency_overrides.clear()


def test_issue_severity_counts_reporter(client, db_session):
    issues = [
        Issue(title="A", description="x", severity="LOW", status="OPEN", reporter_id=2),
        Issue(title="B", description="y", severity="HIGH", status="OPEN", reporter_id=3),
        Issue(title="C", description="z", severity="LOW", status="OPEN", reporter_id=2),
    ]
    db_session.add_all(issues)
    db_session.commit()

    app.dependency_overrides[get_current_user] = override_reporter_user
    response = client.get("/dashboard/issue_severity_counts")
    assert response.status_code == 200
    data = response.json()
    assert data == {"LOW": 2}
    app.dependency_overrides.clear()
