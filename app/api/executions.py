from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.execution import ExecutionRequest
from app.db.models.job import Job as JobModel
from app.db.models.file import File as FileModel
from app.db.models.job_execution import JobExecution as ExecutionModel
from app.services.execution_processor import process_execution
from app.tasks.execution_tasks import process_execution_task
from app.db.models.alert import Alert as AlertModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/execute")
def execute_job(request:ExecutionRequest,db:Session=Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == request.job_id).first()
    if not job:
        return {"error":"Job not found"}
    if not job.is_active:
        return {"error":"Job is not active"}
    file = db.query(FileModel).filter(FileModel.id == request.file_id).first()
    if not file:
        return {"error":"File not found"}
    
    execution_record = ExecutionModel(
        job_id=job.id,
        file_id=file.id,
        error_threshold=job.error_threshold,
        latency_threshold=job.latency_threshold,
    )

    db.add(execution_record)
    db.commit()
    db.refresh(execution_record)
    process_execution_task.delay(str(execution_record.id))
    return {
        "execution_id": execution_record.id,
        "status": execution_record.status,
        "mtrics": {
                "error_threshold": execution_record.error_threshold,
                "latency_threshold": execution_record.latency_threshold,
                "error_count": execution_record.error_count,
                "max_latency": execution_record.max_latency,
                "total_requests": execution_record.total_requests,
        },
        "alerts_generated": execution_record.alerts_generated
    }

@router.post("/executions/{execution_id}/process")
def run_execution(execution_id:str,db:Session=Depends(get_db)):
    try:
        process_execution(execution_id,db)
        return {"message":"Execution processed successfully"}
    except Exception as e:
        return {"error":str(e)}

@router.delete("/executions/{execution_id}")
def delete_execution(execution_id:str,db:Session=Depends(get_db)):
    execution = db.query(ExecutionModel).filter(ExecutionModel.id == execution_id).first()
    if not execution:
        return {"error":"Execution not found"}
    db.delete(execution)
    db.commit()
    return {"message":"Execution deleted successfully"}

@router.delete("/executions")
def delete_all_executions(db:Session=Depends(get_db)):
    db.query(ExecutionModel).delete()
    db.commit()
    return {"message":"All executions deleted successfully"}

@router.delete("/alerts")
def delete_all_alerts(db:Session=Depends(get_db)):
    db.query(AlertModel).delete()
    db.commit()
    return {"message":"All alerts deleted successfully"}