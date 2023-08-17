from app.core.celery_app import celery_app


@celery_app.task
def check_in_db(some):
    """Here we check in db
    """
    return ''.join([let for let in some if let in 'abcd'])
