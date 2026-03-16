from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.job import Job
from app.schemas.job import CreateJobRequest

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/jobs")
def create_job(request: CreateJobRequest, db: Session = Depends(get_db)):

    job = Job(
        name=request.name,
        error_threshold=request.error_threshold,
        latency_threshold=request.latency_threshold,
        is_active=True
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "name": job.name
    }