from app.celery_app import celery_app
from app.schemas import execution
from app.services.execution_processor import process_execution
from app.db.session import SessionLocal

@celery_app.task(bind=True,autoretry_for=(Exception,),retry_backoff=5,retry_kwargs={'max_retries': 3})
def process_execution_task(self, execution_id:str):
    db = SessionLocal()
    try:
        print(f"Processing execution {execution_id}")
        process_execution(execution_id,db)
    except Exception as e:
        execution.status = "FAILED"
        execution.error_message = str(e)
    finally:
        db.close()