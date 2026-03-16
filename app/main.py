from fastapi import FastAPI
import app.db.models
from app.api.files import router as files_router
from app.api.executions import router as executions_router
from app.api.jobs import router as jobs_router

app = FastAPI()

app.include_router(files_router)
app.include_router(executions_router)
app.include_router(jobs_router)