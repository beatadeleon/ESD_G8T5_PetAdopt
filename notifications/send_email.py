import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, message):
    # Email configuration
    sender_email = "beatasanchax@gmail.com"
    body = message

    # Gmail SMTP server configuration
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    # Email login credentials (update with your own)
    username = "beatasanchax@gmail.com "
    password = "mneh mxmf tyyz ftar"

    # Create a MIMEText object for the email content
    msg = MIMEMultipart()
    msg['From'] = 'ESD G8T5 Pet Adopt <beatasanchax@gmail.com>'
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Try to send the email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
    finally:
        server.quit()
