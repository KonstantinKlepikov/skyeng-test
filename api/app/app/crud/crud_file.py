from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas import scheme_file
from app.schemas.constraint import Collections


class CRUDFile(CRUDBase[scheme_file.FileInDb]):
    """Files crud
    """


files = CRUDFile(
    schema=scheme_file.FileInDb,
    col_name=Collections.FILES.value,
    db_name=settings.DB_NAME,
        )
