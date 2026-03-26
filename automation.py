import smtplib
import schedule
import time
import json 
import os
import random
from datetime import datetime,date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
# email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER") or os.getenv("SMPT_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT") or os.getenv("SMPT_PORT")
SMTP_PORT = int(SMTP_PORT) if SMTP_PORT else None

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")
ATTENDANCE_LINK = os.getenv("ATTENDANCE_LINK") or os.getenv("EMAIL_BODY")

EMPLOYEES_FILE = "Employees.json"
HOLIDAYS_FILE="Custom_holidays.json"



#load employees
def load_employees():
    if not os.path.exists(EMPLOYEES_FILE):
        return []
    with open(EMPLOYEES_FILE,"r") as f:
        return json.load(f)
    
def load_quotes():
    if not os.path.exists("QUOTES.json"):
        return []
    with open("QUOTES.json","r") as f:
        return json.load(f)
    
def get_random_quote():
    quotes=load_quotes()
    if not quotes:
        return {"quote":"Have a productive day","author":"HR System"}
    return random.choice(quotes)

def load_holidays():
    if not os.path.exists(HOLIDAYS_FILE):
        return []
    with open(HOLIDAYS_FILE,"r") as f:
        return json.load(f)
def is_working_day():
    today=date.today()

    if today.weekday()==6:
        return False
    
    holidays=load_holidays()
    today_str=today.strftime("%Y-%m-%d")
    
    for h in holidays:
        if h["date"]==today_str:
            return False
    return True
def generate_email(employee_name, quote, author):

    attendance_link = ATTENDANCE_LINK or "https://hr-management-sysytem-production.up.railway.app/"

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body style="margin:0;padding:0;background:#eef3f6;font-family:Arial,Helvetica,sans-serif">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#eef3f6;padding:20px 10px">

<tr>
<td align="center">

<table width="100%" cellpadding="0" cellspacing="0" 
style="max-width:480px;background:#ffffff;border-radius:18px;overflow:hidden;border:1px solid #e3e8ee">

<!-- Header -->

<tr>
<td align="center" style="background:linear-gradient(135deg,#1f7a74,#2e9e95);padding:35px 20px">

<p style="color:white;font-size:26px;font-weight:bold;margin:0;letter-spacing:1px">
START YOUR DAY RIGHT
</p>

<p style="color:#d8f3f1;font-size:14px;margin-top:8px">
Good morning {employee_name}
</p>

</td>
</tr>

<!-- Quote -->

<tr>
<td align="center" style="padding:30px 30px 10px 30px">

<p style="font-size:16px;color:#4c5a57;font-style:italic;line-height:1.6;margin:0">
"{quote}"
</p>

<p style="font-size:14px;color:#1f7a74;font-weight:bold;margin-top:10px">
— {author}
</p>

</td>
</tr>

<!-- Divider -->

<tr>
<td align="center" style="padding:10px 40px">
<hr style="border:none;border-top:1px solid #e7ecef">
</td>
</tr>

<!-- Attendance Title -->

<tr>
<td align="center" style="padding:10px 30px 10px 30px">

<p style="font-size:18px;color:#234F4A;font-weight:bold;margin:0">
MARK YOUR ATTENDANCE
</p>

<p style="font-size:13px;color:#7a8785;margin-top:6px">
Scan the QR or tap the button below
</p>

</td>
</tr>

<!-- QR -->

<tr>
<td align="center" style="padding:15px 30px">

<img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data={attendance_link}"
width="160"
style="border:1px solid #dde4ea;padding:12px;border-radius:10px;background:#f9fbfc">

</td>
</tr>

<!-- Button -->

<tr>
<td align="center" style="padding:10px 30px 35px 30px">

<a href="{attendance_link}"
style="
display:inline-block;
background:#d9a860;
color:white;
font-weight:bold;
font-size:15px;
padding:14px 28px;
border-radius:10px;
text-decoration:none;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
">
MARK ATTENDANCE
</a>

</td>
</tr>

<!-- Footer -->

<tr>
<td align="center" style="background:#f6faf9;padding:25px 20px">

<p style="font-size:13px;color:#5c6b69;margin:0">
YOUR JOURNEY. YOUR EFFORT.
</p>

<p style="font-size:14px;color:#1f7a74;font-weight:bold;margin-top:6px">
#StayConsistent
</p>

<p style="font-size:11px;color:#9aa5a3;margin-top:15px">
Made with ❤️ by Omkar
</p>

</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

    return html
def send_emails():

    if not is_working_day():
        return

    if not SMTP_SERVER or not SMTP_PORT or not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Missing SMTP configuration in environment variables")
        return

    employees = load_employees()

    if not employees:
        print("No employees found")
        return

    quote_data = get_random_quote()

    quote = quote_data["quote"]
    author = quote_data["author"]

    print("Sending emails to", len(employees), "employees")
    try:

        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()

        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for emp in employees:

            msg = MIMEMultipart()

            msg["From"] = SENDER_EMAIL
            msg["To"] = emp["email"]
            msg["Subject"] = EMAIL_SUBJECT or "Daily Check-in Reminder"

            html = generate_email(emp["name"], quote, author)

            msg.attach(MIMEText(html, "html"))

            server.send_message(msg)

            print("Email sent to:", emp["email"])

        server.quit()

    except Exception as e:
        print("Email error:", e)


def job():

    print("Running job at", datetime.now())

    send_emails()


if __name__ == "__main__":

    print("EMAIL AUTOMATION SYSTEM STARTED")

    schedule.every().day.at("09:30").do(job)

    while True:

        schedule.run_pending()

        time.sleep(60)

