from pydantic import BaseModel
from uuid import UUID

class ExecutionRequest(BaseModel):
    job_id:UUID
    file_id:UUID