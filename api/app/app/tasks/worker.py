import asyncio
from typing import Any
# from celery.schedules import crontab
from pydantic import  EmailStr
from app.core.celery_app import celery_app
from app.core.core_email import send_email
from app.crud.crud_file import files, files_raw
from app.db.init_db import BdContext, client


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        query_in_db.s(),
        name='check-solutions'
            )


async def get_unchecked_raw() -> list[dict[str, Any]]:
    """"""
    async with BdContext(client) as db:

        not_checked = await files.get_many(
            db=db,
            q={'is_checked': False, 'is_deleted_by_user': False}
                )
        tasks = [
            asyncio.create_task(files_raw.get(db=db, q={'file_id': str(i['_id'])}))
            for i in
            not_checked
                ]
        results = [await task for task in tasks]
        return results


@celery_app.task
def query_in_db() -> dict[str, str]:
    """Query data for chedulercheck in db
    """
    result = asyncio.get_event_loop().run_until_complete(
        get_unchecked_raw()
            )
    return result # FIXME: run many chain tasks


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
