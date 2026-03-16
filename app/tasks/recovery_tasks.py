from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.recovery_service import recover_stale_executions

@celery_app.task
def recover_stale_execution():
    db = SessionLocal()
    try:
        recover_stale_executions(db)
    finally:
        db.close()