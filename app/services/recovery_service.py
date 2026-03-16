from sqlalchemy.orm import Session
from datetime import datetime,timedelta, timezone
from app.db.models.job_execution import JobExecution
from app.tasks.execution_tasks import process_execution_task

execution_timeout_seconds = 300

def recover_stale_executions(db:Session):
    timeout = datetime.now(timezone.utc) - timedelta(seconds=execution_timeout_seconds)
    stale_executions = db.query(JobExecution).filter(JobExecution.status == 'RUNNING', JobExecution.started_at < timeout).all()

    for execution in stale_executions:
        execution.status = 'PENDING'
        execution.started_at = None
        db.commit()

        process_execution_task.delay(str(execution.id))