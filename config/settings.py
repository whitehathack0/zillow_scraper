# Redis.
import os

SECRET_KEY = os.getenv("SECRET_KEY", None)

REDIS_URL = os.getenv("REDIS_URL", "redis://0.0.0.0:6379/0")

# Celery.
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": ["app.tasks"],
}
