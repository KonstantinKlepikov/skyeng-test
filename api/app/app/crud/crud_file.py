from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas import scheme_file
from app.schemas.constraint import Collections


class CRUDFile(CRUDBase[scheme_file.File]):
    """Files crud
    """


class CRUDFileRaw(CRUDBase[scheme_file.FileRaw]):
    """Files raw crud
    """


files = CRUDFile(
    schema=scheme_file.File,
    col_name=Collections.FILES.value,
    db_name=settings.DB_NAME,
        )

files_raw = CRUDFileRaw(
    schema=scheme_file.FileRaw,
    col_name=Collections.FILES_RAW.value,
    db_name=settings.DB_NAME,
        )
