# app/tasks/notification_tasks.py

from app.celery_app import celery
from app.extensions import mail
from flask_mail import Message

BASE_URL = "http://localhost:5000"   


@celery.task(name='app.tasks.notification_tasks.send_staff_welcome_email')
def send_staff_welcome_email(staff_email, staff_name, temp_password):
    
    try:
        msg = Message(
            subject="Welcome to BookYourTreks — Your Staff Account",
            recipients=[staff_email],
            body=(
                f"Hi {staff_name},\n\n"
                f"You have been added as Trekking Staff on BookYourTreks.com.\n\n"
                f"Login Email: {staff_email}\n"
                f"Temporary Password: {temp_password}\n\n"
                f"Please log in and change your password from your profile.\n\n"
                f"— BookYourTreks Team"
            )
        )
        mail.send(msg)
        return f"Welcome email sent to {staff_email}"
    except Exception as e:
        return f"Failed to send staff welcome email: {e}"


@celery.task(name='app.tasks.notification_tasks.send_trek_assignment_email')
def send_trek_assignment_email(staff_email, staff_name, trek_name, trek_location, start_date):
    
    try:
        msg = Message(
            subject=f"New Trek Assigned: {trek_name}",
            recipients=[staff_email],
            body=(
                f"Hi {staff_name},\n\n"
                f"You have been assigned to manage a new trek:\n\n"
                f"Trek: {trek_name}\n"
                f"Location: {trek_location}\n"
                f"Start Date: {start_date}\n\n"
                f"Please log in to your dashboard to view details and manage slots.\n\n"
                f"— BookYourTreks Team"
            )
        )
        mail.send(msg)
        return f"Assignment email sent to {staff_email}"
    except Exception as e:
        return f"Failed to send assignment email: {e}"


@celery.task(name='app.tasks.notification_tasks.send_booking_confirmation_email')
def send_booking_confirmation_email(user_email, user_name, trek_name, booking_id):
    
    payment_link = f"{BASE_URL}/api/customer/payment/confirm/{booking_id}"
    try:
        msg = Message(
            subject=f"Booking Confirmed — {trek_name}",
            recipients=[user_email],
            html=f"""
                <p>Hi {user_name},</p>
                <p>Your booking for <b>{trek_name}</b> has been placed successfully.</p>
                <p>Payment Status: <b>Pending</b></p>
                <p>Please complete your payment to confirm your slot:</p>
                <p><a href="{payment_link}" style="background:#0f766e;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:6px;">Pay Now (Demo)</a></p>
                <p>— BookYourTreks Team</p>
            """
        )
        mail.send(msg)
        return f"Booking confirmation sent to {user_email}"
    except Exception as e:
        return f"Failed to send booking email: {e}"