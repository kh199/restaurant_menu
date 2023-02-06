from celery import Celery

from app.core.config import BROKER_URL

celery = Celery(
    "tasks", backend="rpc://", broker=BROKER_URL, include=["app.report.tasks"]
)
celery.conf.task_default_queue = "celery"
celery.conf.accept_content = ["application/json", "application/x-python-serialize"]
celery.autodiscover_tasks()
