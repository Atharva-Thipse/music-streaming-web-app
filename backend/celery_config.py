from celery import Celery
from celery.schedules import crontab

# Initialize Celery with Redis broker and backend
celery = Celery(__name__, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

# Define the Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'generate_monthly_report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=8, minute=0),
    },
    'update-visited': {
        'task': 'tasks.update_visited',
        'schedule': crontab(hour=20, minute=0),
    },
    'generate_daily_report': {
        'task': 'tasks.generate_daily_report',
        'schedule': crontab(hour=19, minute=0),
    },
}

# Set the Celery beat schedule
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE