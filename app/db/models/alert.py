import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint
from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("job_executions.id"), nullable=False)

    alert_type = Column(String, nullable=False)
    metric_value = Column(Float)
    threshold = Column(Float)
    sample_count = Column(Integer)
    message = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("execution_id", "alert_type", name="uq_execution_alert"),
    )