# app/tasks/report_tasks.py

from datetime import datetime, timedelta
from app.celery_app import celery
from app.extensions import mail
from flask_mail import Message


@celery.task(name='app.tasks.report_tasks.generate_monthly_report')
def generate_monthly_report():

    from app.models.trek import Trek, TrekStatusEnum
    from app.models.booking import Booking, BookingStatusEnum
    from app.models.user import User, RoleEnum

    today = datetime.today()
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    completed_treks = Trek.query.filter(
        Trek.status == TrekStatusEnum.COMPLETED,
        Trek.end_date >= last_month_start.date(),
        Trek.end_date <= last_month_end.date()
    ).all()

    total_bookings = Booking.query.filter(
        Booking.created_at >= last_month_start,
        Booking.created_at <= last_month_end
    ).count()

    cancelled_bookings = Booking.query.filter(
        Booking.status == BookingStatusEnum.CANCELLED,
        Booking.created_at >= last_month_start,
        Booking.created_at <= last_month_end
    ).count()

    # popular treks — sabse zyada bookings wale top 5
    popular_treks = sorted(completed_treks, key=lambda t: t.registered_users_count(), reverse=True)[:5]

    admin = User.query.filter_by(role=RoleEnum.ADMIN).first()
    if not admin:
        return "No admin found to send report to"

    html_body = f"""
    <h2>Monthly Trekking Activity Report</h2>
    <p><b>Period:</b> {last_month_start.strftime('%B %Y')}</p>
    <p><b>Treks Conducted:</b> {len(completed_treks)}</p>
    <p><b>Total Bookings:</b> {total_bookings}</p>
    <p><b>Cancelled Bookings:</b> {cancelled_bookings}</p>
    <h3>Popular Treks</h3>
    <ul>
        {''.join(f"<li>{t.name} — {t.registered_users_count()} participants</li>" for t in popular_treks)}
    </ul>
    """

    try:
        msg = Message(
            subject=f"Monthly Trekking Report — {last_month_start.strftime('%B %Y')}",
            recipients=[admin.email],
            html=html_body
        )
        mail.send(msg)
        return f"Monthly report sent to {admin.email}"
    except Exception as e:
        return f"Failed to send report: {e}"