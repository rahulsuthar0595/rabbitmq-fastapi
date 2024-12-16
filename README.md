# Celery with FastAPI

### Run this commands for celery, flower and beat:

celery -A workers.worker beat --loglevel=info

celery -A workers.worker worker --loglevel=info

celery -A workers.worker flower --loglevel=info
