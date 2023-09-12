import asyncio
import tempfile
from typing import Any
from bson import ObjectId
from app.core.celery_app import celery_app
from app.core.core_email import send_email
from app.crud.crud_file import files, files_raw
from app.crud.crud_user import users
from app.db.init_db import BdContext, client
from app.config import settings


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        settings.TIME_TO_CHECK,
        query_in_db.s(),
        name='check-solutions'
            )


async def get_unchecked_raw() -> list[dict[str, Any]]:
    """Get unchecked raw files from db and pipe it to tasks

    Returns:
        list[dict[str, Any]] - db data
    """
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


async def get_send_save(check: dict[str, Any]) -> None:
    """"""""
    async with BdContext(client) as db:
        # TODO:  here we need a transaction

        # get user
        user = await users.get(db, {'_id': ObjectId(check['user_id'])})

        # fix result in db
        update = await files.update(
            db=db,
            q={'_id': ObjectId(check['file_id'])},
            obj_in={'is_checked': True, 'is_email_sended': True}
                )

        if update.matched_count != 0:

            # send email
            await send_email(
                check['result'],
                user['email'],
                settings.MAIL_FROM_NAME
                    )

        # TODO: close transaction


@celery_app.task
def query_in_db() -> None:
    """Query data for chedulercheck in db
    """
    result = asyncio.get_event_loop().run_until_complete(
        get_unchecked_raw()
            )
    for check in result:
        check['_id'] = str(check['_id'])  # FIXME:
        chain = make_flake_check.s(check) | celery_save_and_mail.s()
        chain()


@celery_app.task
def make_flake_check(check: dict[str, Any]) -> dict[str, bool | str]:
    """Make flake8 check
    """
    # create temporal file
    with tempfile.TemporaryFile() as f:
        f.write(check['raw'].encode('utf-8'))
        f.seek(0)

        # TODO: use some checks with temporal file here

        # fix result of check
        check['result'] = 'Check result'

    if check.get('result'):
        return check
    raise KeyError('No walid result')


@celery_app.task
def celery_save_and_mail(check: dict[str, Any]) -> None:
    """Send email with result of check and save to db
    """
    asyncio.get_event_loop().run_until_complete(
        get_send_save(check)
            )
