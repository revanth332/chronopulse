
import os
import uuid
import hashlib
from fastapi import UploadFile

UPLOAD_DIR = 'uploads'

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file:UploadFile):
    file_id = uuid.uuid4()
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR,file_name)
    hasher = hashlib.sha256()
    with open(file_path, "wb") as f:
        while chunk := file.file.read(1024 * 1024):
            f.write(chunk)
            hasher.update(chunk)
    checksum = hasher.hexdigest()
    file_size = os.path.getsize(file_path)

    return {
        "file_name":file_name,
        "file_path":file_path,
        "size_bytes":file_size,
        "checksum":checksum,
        "storage_path":file_path
    }