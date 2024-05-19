import os
from django.conf import settings


def get_logging_dir(log_name: str = 'log') -> str:
    log_dir = f"{settings.BASE_DIR}/log"
    os.makedirs(log_dir, exist_ok=True)
    return f"{log_dir}/{log_name}.log"
