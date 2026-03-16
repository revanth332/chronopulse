
from sqlalchemy.orm import Session
from app.db.models.job_execution import JobExecution
from app.db.models.file import File as FileModel
from datetime import datetime, timezone
from app.db.models.alert import Alert as AlertModel

def process_execution(execution_id:str,db:Session):
    execution = db.query(JobExecution).filter(JobExecution.id == execution_id).first()
    if not execution:
        raise Exception("Execution not found")
    if execution.status == 'SUCCESS':
        return
    
    execution.status = 'RUNNING'
    execution.started_at = datetime.now(timezone.utc)
    db.commit()

    error_count = 0
    max_latency = 0
    total_requests = 0
    file_path = db.query(FileModel).filter(FileModel.id == execution.file_id).first().storage_path
    with open(file_path, 'r') as f:
        for line in f:
            total_requests += 1
            parts = line.strip().split()
            latency = int(parts[3].replace('ms',''))
            status_code = int(parts[2])
            if status_code >= 500:
                error_count += 1
            max_latency = max(max_latency, latency)
    if total_requests == 0:
        raise Exception("No requests found in file")
    alerts = []
    if execution.error_threshold:
        error_rate = (error_count / total_requests)*100
        if error_rate > execution.error_threshold:
            alerts.append({
                "alert_type": "ERROR_RATE_HIGH",
                "metric_value": error_rate,
                "message": f"Error rate {error_rate:.2f}% exceeded threshold {execution.error_threshold}%"
            })
    if execution.latency_threshold:
        if max_latency > execution.latency_threshold:
            alerts.append({
                "alert_type": "LATENCY_HIGH",
                "metric_value": max_latency,
                "message": f"Max latency {max_latency}ms exceeds threshold {execution.latency_threshold}ms"
            })

    for alert in alerts:
        db.add(AlertModel(
            execution_id=execution.id,
            alert_type=alert["alert_type"],
            metric_value=alert["metric_value"],
            threshold=execution.error_threshold if alert["alert_type"] == "ERROR_RATE_HIGH" else execution.latency_threshold,
            sample_count=total_requests,
            message=alert["message"]
        ))
    execution.status = 'SUCCESS'
    execution.error_count = error_count
    execution.max_latency = max_latency
    execution.alerts_generated = len(alerts)
    execution.total_requests = total_requests
    execution.completed_at = datetime.now(timezone.utc)
    db.commit()
    