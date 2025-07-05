import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_upload_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    destination = os.path.join(UPLOAD_DIR, unique_name)
    with open(destination, "wb") as buffer:
        buffer.write(file.file.read())
    return destination  
