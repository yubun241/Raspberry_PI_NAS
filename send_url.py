import smtplib
from email.mime.text import MIMEText
import sys
import datetime

gmail = ""
app_password = ""

url = sys.argv[1]
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

body = f"""Mobile S3 Server Started

Time:
{now}

URL:
{url}
"""

msg = MIMEText(body)
msg["Subject"] = "Mobile S3 Server URL"
msg["From"] = gmail
msg["To"] = gmail

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(gmail, app_password)
server.send_message(msg)
server.quit()

print("Mail sent")
