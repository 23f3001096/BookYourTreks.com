# app/tasks/export_tasks.py

import os
import csv
import uuid
from app.celery_app import celery

EXPORT_DIR = os.path.join(os.getcwd(), 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)


@celery.task(name='app.tasks.export_tasks.generate_csv_export', bind=True)
def generate_csv_export(self, user_id):
    from app.models.booking import Booking

    bookings = Booking.query.filter_by(user_id=user_id).all()

    filename = f"booking_history_{user_id}_{uuid.uuid4().hex[:8]}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Trek Name", "Location", "Booking Status", "Start Date", "End Date", "Booking Date"])
        for b in bookings:
            writer.writerow([
                b.user_id,
                b.trek.name if b.trek else "",
                b.trek.location if b.trek else "",
                b.status.value,
                b.trek.start_date if b.trek else "",
                b.trek.end_date if b.trek else "",
                b.created_at.strftime('%Y-%m-%d') if b.created_at else "",
            ])

    return {"filename": filename, "filepath": filepath}