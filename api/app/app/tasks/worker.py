import asyncio
# from celery.schedules import crontab
from pydantic import  EmailStr
from app.core.celery_app import celery_app
from app.core.core_email import send_email


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        query_in_db.s('hello'),
        name='check-solutions'
            )


@celery_app.task
def query_in_db(id: str) -> dict[str, str]:
    """Query data for chedulercheck in db
    """
    # query db for file data
    return {'result': id}


@celery_app.task
def make_flake_check(to_check: str) -> str:
    """Make flake8 check
    """
    # create temporal file

    # use flake8 for check

    # get result and return it as text


@celery_app.task
def save_result(resul_of_check: str) -> str:
    """Save result in db
    """
    # query to save


@celery_app.task(name="celery-mail", bind=True)
def send_email(message: str) -> None:
    """Send email with result of check
    """


@celery_app.task(name="celery-mail", bind=True)
def celery_mail(message: str, recipient: EmailStr, subject: str):
    asyncio.run(send_email(message, recipient, subject))
