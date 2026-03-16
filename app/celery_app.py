from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'chronopulse',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    imports=["app.tasks.execution_tasks"]
)

celery_app.conf.beat_schedule = {
    "recover-stale-executions": {
        "task": "app.tasks.recovery_tasks.recover_stale_executions_task",
        "schedule": 20.0,
    },
}