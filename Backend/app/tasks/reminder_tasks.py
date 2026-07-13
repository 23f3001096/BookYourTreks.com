# app/tasks/reminder_tasks.py

from datetime import date, timedelta
from app.celery_app import celery
from app.extensions import mail
from flask_mail import Message


@celery.task(name='app.tasks.reminder_tasks.send_daily_reminders')
def send_daily_reminders():

    from app.models.trek import Trek
    from app.models.booking import Booking, BookingStatusEnum

    tomorrow = date.today() + timedelta(days=1)
    upcoming_treks = Trek.query.filter_by().all()
    print("*************************")
    print(upcoming_treks)

    sent_count = 0
    for trek in upcoming_treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, status=BookingStatusEnum.BOOKED).all()
        for booking in bookings:
            try:
                msg = Message(
                    subject=f"Reminder: {trek.name} starts tomorrow!",
                    recipients=[booking.user.email],
                    body=(
                        f"Hi {booking.user.name},\n\n"
                        f"Your trek '{trek.name}' at {trek.location} starts tomorrow "
                        f"({trek.start_date}).\n"
                        f"Duration: {trek.duration_days} days\n"
                        f"Difficulty: {trek.difficulty.value}\n\n"
                        f"Please be prepared and arrive on time. Happy trekking!"
                    )
                )
                mail.send(msg)
                sent_count += 1
            except Exception as e:
                print(f"Failed to send reminder to {booking.user.email}: {e}")

    return f"Sent {sent_count} reminders for {len(upcoming_treks)} treks"