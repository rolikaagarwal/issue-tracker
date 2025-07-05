import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

os.environ["ENV"] = "test"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database.base_class import Base
from app.dependencies.auth import get_db, get_current_user
from app.models.issues import Issue
from app.models.user import User, RoleEnum
from app.models.attachment import FileAttachment
from app.core.security import PasswordHasher, JWTAuth

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Auto fixture to drop & create tables once per test session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_session():
    """Yields a DB session usable across tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Provides a test client and fresh DB for each test function."""
    for model in [FileAttachment, Issue, User]:
        db_session.query(model).delete()
    db_session.commit()

    test_user = User(
        id=1,
        email="test@example.com",
        role=RoleEnum.ADMIN,
        hashed_password=PasswordHasher.hash("irrelevant")
    )
    db_session.add(test_user)
    db_session.commit()

    def override_get_db():
        yield db_session

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    return TestClient(app)


@pytest.fixture
def create_user(db_session):
    """Factory to create users in DB."""
    def _create(email: str, password: str = "testpass", role: RoleEnum = RoleEnum.REPORTER, user_id: int = None):
        try:
            user = User(
                email=email,
                role=role,
                hashed_password=PasswordHasher.hash(password)
            )
            if user_id:
                user.id = user_id
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except Exception:
            db_session.rollback()
            raise
    return _create


@pytest.fixture
def auth_token(create_user):
    """Factory to generate JWT access token for a user."""
    def _generate(email="auth@example.com", password="testpass", role=RoleEnum.REPORTER):
        user = create_user(email=email, password=password, role=role)
        return JWTAuth.create_token(data={"sub": str(user.id), "role": user.role.value})
    return _generate
