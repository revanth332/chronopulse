from fastapi import APIRouter,UploadFile,File,Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.storage.local_storage import save_file
from app.db.models.file import File as FileModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/file")
def upload_file(file:UploadFile = File(...),db:Session = Depends(get_db)):
    file_info = save_file(file)

    file_record = FileModel(
        filename=file_info['file_name'],
        size_bytes=file_info['size_bytes'],
        checksum=file_info['checksum'],
        storage_path=file_info['storage_path']
    )

    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return {
        "id": file_record.id,
        "filename": file_record.filename,
        "size_bytes": file_record.size_bytes,
    }