from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas import scheme_user
from app.schemas.constraint import Collections


class CRUDUser(CRUDBase[scheme_user.UserInDb]):
    """Users crud
    """


users = CRUDUser(
    schema=scheme_user.UserInDb,
    col_name=Collections.USERS.value,
    db_name=settings.DB_NAME,
        )
