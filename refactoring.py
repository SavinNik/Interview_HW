import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"

    def __init__(self, smtp_server, imap_server, email_address, password):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = password

    def send_email(self, recipients, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, recipients, msg.as_string())

    def receive_email(self, header=None):
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.email_address, self.password)
            mail.select("inbox")
            criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
            result, data = mail.uid('search', '', criterion)

            if not data[0]:
                raise ValueError('There are no letters with current header')

            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email)
            return email_message


if __name__ == '__main__':
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"
    EMAIL_ADDRESS = 'login@gmail.com'
    PASSWORD = 'qwerty'

    client = EmailClient(smtp_server=GMAIL_SMTP, imap_server=GMAIL_IMAP, email_address=EMAIL_ADDRESS, password=PASSWORD)

    recipients_list = ['vasya@email.com', 'petya@email.com']
    subject_ = 'Subject'
    message_ = 'Message'

    client.send_email(recipients_list, subject_, message_)

    try:
        received_email = client.receive_email(subject_)
        print(received_email)
    except ValueError as error:
        print(error)
