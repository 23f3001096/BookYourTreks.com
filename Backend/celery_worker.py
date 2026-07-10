# celery_worker.py

from app import create_app
from app.celery_app import celery

import app.tasks.reminder_tasks
import app.tasks.report_tasks
import app.tasks.export_tasks

flask_app = create_app()
flask_app.app_context().push()