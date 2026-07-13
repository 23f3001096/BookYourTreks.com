# BookYourTreks.com

A Trekking Management Application (TMA) where Admin, Trek Staff, and Trekkers (Users) can manage and book trekking activities — trek approvals, participant registrations, slot availability, and booking tracking, all in one place.

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** VueJS (CDN) + Vue Router + Bootstrap
- **Database:** SQLite
- **Caching:** Redis
- **Background Jobs:** Redis + Celery
- **Email:** Flask-Mail (Mailpit for local testing)

## Prerequisites

Make sure these are installed on your machine (WSL/Linux) before starting:

- Python 3.10+
- Redis
- Mailpit (local SMTP testing server)

### Install Redis

```bash
sudo apt update
sudo apt install redis-server -y
```

### Install Mailpit

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/axllent/mailpit/develop/install.sh)"
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd BookYourTreks.com/Backend
```

### 2. Create and activate a virtual environment

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip install python-dotenv flask celery flask_sqlalchemy flask_login redis flask_mail
```

### 4. Set up environment variables

## Running the Application

The app needs **4 things running at the same time**, each in its own terminal tab.

### Terminal 1 — Redis

```bash
redis-server
```

### Terminal 2 — Mailpit (email testing UI)

```bash
mailpit
```
Once running, open **http://localhost:8025** in your browser to view all emails the app sends (staff welcome emails, trek assignment notices, booking confirmations, monthly reports, etc).

### Terminal 3 — Flask App

```bash
cd Backend
source .venv/bin/activate
python3 run.py
```
The app will be available at **http://localhost:5000**

### Terminal 4 — Celery Worker

```bash
cd Backend
source .venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```
This handles background jobs — CSV export, booking confirmation emails, trek assignment emails, staff welcome emails.

### Terminal 5 — Celery Beat (scheduled jobs)

```bash
cd Backend
source .venv/bin/activate
celery -A celery_worker.celery beat --loglevel=info
```
This triggers the two scheduled jobs automatically:
- **Daily reminders** — sent every day to users with treks starting the next day
- **Monthly activity report** — sent to Admin on the 1st of every month

> Terminals 4 and 5 are only needed if you want to test the scheduled/background email features. The core app (login, booking, treks, etc.) works fine without them — booking and staff-creation emails simply won't send if Celery isn't running, but nothing will break.

## Default Admin Login

An admin account is created automatically the first time the app runs:

```
Email: admin@gmail.com
Password: admin123
```

There is no admin registration route — only this one pre-seeded admin exists. Trek Staff accounts can only be created by this Admin from the dashboard.

## Project Roles

| Role | Access |
|---|---|
| **Admin** | Manage treks, staff, users, view reports & bookings |
| **Trek Staff** | Manage assigned treks, update slots/status, view participants |
| **User (Trekker)** | Browse & book treks, manage bookings, write reviews |

## Stopping the App

Press `Ctrl+C` in each terminal to stop the respective service. To fully reset the database during development:

```bash
cd Backend
rm trekking.db
python3 run.py
```
This recreates the database and re-seeds the default admin.

## Testing the CSV Export / Email Features

1. Make sure Redis, Mailpit, Flask, and the Celery worker are all running.
2. Log in as a customer, book a trek.
3. Check **http://localhost:8025** — a booking confirmation email (with a demo "Pay Now" link) should appear.
4. From "Trekking History", click **Export CSV** — it will process in the background and auto-download once ready.

## Troubleshooting

**"database is locked" error:**
Usually means an old Python shell or duplicate Flask process is still holding the SQLite file open. Check with:
```bash
lsof | grep trekking.db
```
Kill any stray processes and restart.

**Emails not appearing in Mailpit:**
Confirm Mailpit is running (`mailpit` command) and `.env` has `MAIL_SERVER=localhost`, `MAIL_PORT=1025`.

**Redis connection errors:**
Confirm Redis is running with `redis-cli ping` — it should reply `PONG`.