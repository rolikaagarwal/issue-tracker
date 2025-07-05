from sqlalchemy.orm import Session
from app.models.attachment import FileAttachment

class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_issue_with_attachment(self, issue_id: int, filename: str, filepath: str):
        attachment = FileAttachment(issue_id=issue_id, filename=filename, filepath=filepath)
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment
