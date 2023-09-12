from celery import Celery
from app.config import settings


celery_app = Celery(
    "worker",
    # broker=settings.MONGODB_URL.get_secret_value(),
    beiker=settings.CELERY_BROKER_URL,
    include=['app.tasks', ],
        )
