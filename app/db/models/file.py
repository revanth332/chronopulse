import uuid
from sqlalchemy import Column, String, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String,nullable=False)
    size_bytes = Column(BigInteger,nullable=False)
    checksum = Column(String,nullable=False)
    storage_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)