from celery import Celery
from app.config import settings


celery_app = Celery(
    "worker",
    beiker=settings.CELERY_BROKER_URL,
    include=['app.tasks', ],
        )
