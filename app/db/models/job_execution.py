import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint
from app.db.base import Base

class JobExecution(Base):
    __tablename__ = "job_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)

    # Snapshot config
    error_threshold = Column(Float)
    latency_threshold = Column(Integer)

    status = Column(String, nullable=False, default="PENDING")
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("job_id", "file_id", name="uq_job_file"),
    )