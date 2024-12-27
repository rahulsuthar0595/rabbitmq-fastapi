# Celery with FastAPI

### Run this commands for celery, flower and beat:

celery -A workers.celery_config beat --loglevel=info

celery -A workers.celery_config worker --loglevel=info

celery -A workers.celery_config flower --loglevel=info
