from app.config import settings
from app.schemas import constraint


# save tasks and results to mongodb
result_backend = settings.MONGODB_URL.get_secret_value()
mongodb_backend_settings = {
    'database': settings.DB_NAME,
    'taskmeta_collection': constraint.Collections.FILES_CHECK.value,
        }

# TODO: remove this file
