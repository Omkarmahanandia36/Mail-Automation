# Mail Automation

Sends a daily attendance reminder email to all employees listed in `Employees.json`.

## Setup

1. Create a `.env` file in the project root (see `.env` example below).
2. Install dependencies:

```powershell
pip install python-dotenv schedule
```

## .env

```env
# Email configuration
SENDER_EMAIL=yourgmail@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# Email Content
EMAIL_SUBJECT=Daily Check-in Reminder
ATTENDANCE_LINK=https://hr-management-sysytem-production.up.railway.app/
```

Notes:
- For Gmail, use an **App Password** (not your normal password). You must enable 2‑Step Verification to create one.
- Port `465` uses SSL. Port `587` uses STARTTLS. The script supports both.

## Employees

Edit `Employees.json` to control recipients. Example:

```json
[
  {"name": "Omkar Mahanandia", "email": "omkaroditech@gmail.com", "dob": "02.12.2001"}
]
```

## Quotes

Quotes are loaded from `QUOTES.json`:

```json
[
  {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"}
]
```

## Holidays

`Custom_holidays.json` contains dates that should be skipped. The script also skips Sundays.

Date format: `YYYY-MM-DD`

## Run

Start the scheduler (runs continuously):

```powershell
python automation.py
```

To send a one‑off email immediately:

```powershell
@'
import automation
automation.send_emails()
'@ | python -
```

## Schedule Time

Edit the scheduled time in `automation.py`:

```python
schedule.every().day.at("15:20").do(job)
```

The time uses your system’s local timezone.

## GitHub Actions

You can run the email send on a daily schedule using GitHub Actions.

1. Push this repo to GitHub.
2. Add repository secrets (Settings → Secrets and variables → Actions):
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD`
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `EMAIL_SUBJECT` (optional)
   - `ATTENDANCE_LINK` (optional)
3. The workflow runs daily at **15:20 Asia/Kolkata** (09:50 UTC).  
   Edit `.github/workflows/email.yml` if you want a different time.

Note: GitHub Actions uses secrets, not `.env`. Keep real credentials out of the repo.

## Troubleshooting

**SMTP blocked (WinError 10013)**  
Your network may block outbound SMTP. Try:
- Allow outbound port `587` or `465` in Windows Firewall.
- Use a different network (mobile hotspot).

**Gmail 535 BadCredentials**  
Use an App Password and make sure `SENDER_EMAIL` matches the Gmail account that created it.
