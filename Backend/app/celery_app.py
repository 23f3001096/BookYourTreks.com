# app/celery_app.py

from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__)


def init_celery(app):
    """App config se Celery ko configure karta hai, aur Flask app context
    ke andar tasks chalne ki guarantee deta hai."""
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone=app.config['CELERY_TIMEZONE'],
        enable_utc=False,
    )

    # ---------- Scheduled tasks (Celery Beat) ----------
    celery.conf.beat_schedule = {
        'daily-trek-reminders': {
            'task': 'app.tasks.reminder_tasks.send_daily_reminders',
            'schedule': crontab(hour=8, minute=0),  
        },
        'monthly-activity-report': {
            'task': 'app.tasks.report_tasks.generate_monthly_report',
            'schedule': crontab(day_of_month=1, hour=6, minute=0), 
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery