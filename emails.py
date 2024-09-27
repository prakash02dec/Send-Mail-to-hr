import smtplib
import os
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body, to_email, attachment_paths):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject


    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in attachment_paths:
        part = MIMEBase('application', 'octet-stream')
        filename = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        msg.attach(part)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    text = msg.as_string()
    server.sendmail(from_email, to_email, text)

    server.quit()


def schedule_email(subject, body, to_email, attachment_path, send_datetime):
    print(f"Email scheduled for {send_datetime}")

    while True:
        now = datetime.now()

        if now >= send_datetime:
            send_email(subject, body, to_email, attachment_path)
            print(f"Email sent at {now}")
            break

        time.sleep(60)

if __name__ == "__main__":
    df = pd.read_csv("hr_contacts.csv")
    body_template = open("email_template.txt").read()
    subject = os.getenv("EMAIL_SUBJECT")
    for idx, detail in df.iloc[400:800].iterrows():
        to_email = detail.iloc[2].strip()
        name = detail.iloc[1]
        header = f"Dear {name},"
        body = f"{header}\n\n{body_template}"
        attachment_paths = ["./Prakash_Agarwal_Software_Developer.pdf",]  ## Add more attachments here or resume
        today = datetime.now()
        schedule_email(subject, body, to_email, attachment_paths, today)