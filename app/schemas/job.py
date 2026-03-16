from pydantic import BaseModel
from typing import Optional


class CreateJobRequest(BaseModel):
    name: str
    error_threshold: Optional[float] = None
    latency_threshold: Optional[int] = None