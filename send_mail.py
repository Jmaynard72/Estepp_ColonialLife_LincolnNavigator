import smtplib
from email.message import EmailMessage

def send_message(sendTo: str, subject: str, bodyText: str):
    # Connection Parameters
    SMTP_Server = 'smtp.office365.com'
    SMTP_Port = 587
    Email_Sender = 'payrollreports@payrollsolutions.cc'
    Email_Password = '6a3233bA42?'

    msg = EmailMessage()
    msg.set_content(bodyText)
    msg['Subject'] = subject
    msg['From'] = Email_Sender
    msg['To'] = sendTo

    try:
        with smtplib.SMTP(SMTP_Server,SMTP_Port) as server:
            server.starttls()
            server.login(Email_Sender,Email_Password)
            server.send_message(msg)
    except Exception as e:
        print(f'Error sending message: {e}')
        