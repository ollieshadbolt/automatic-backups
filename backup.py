import datetime
import os
import json
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = str(datetime.datetime.now())
script_dir = os.path.dirname(os.path.realpath(__file__))


def get_dir(filename):
    return os.path.join(script_dir, filename)


with open(get_dir("body.html"), encoding="utf8") as body_html:
    body = body_html.read()

with open(get_dir("login.json")) as login_json:
    login = json.load(login_json)

sender_email = login["sender_email"]
password = login["password"]

with open(get_dir("receiver_email.txt")) as receiver_email_txt:
    receiver_email = receiver_email_txt.readlines()

receiver_email = [_[:-1] for _ in receiver_email]

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "html"))

filename = "ollie_shadbolt.kdbx"  # In same directory as script

# Open PDF file in binary mode
with open(get_dir(filename), "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
