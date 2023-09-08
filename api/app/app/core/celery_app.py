from celery import Celery
from app.config import settings


celery_app = Celery(
    "worker",
    # broker=settings.CELERY_BROKER_URL,
    broker=settings.MONGODB_URL.get_secret_value(),
    # backend='rpc://',
    include=['app.tasks', ],
        )
default_config = 'app.core.celeryconfig' # FIXME: remove result backend
celery_app.config_from_object(default_config)
