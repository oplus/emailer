import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError


class emailer:
    def __init__(self, html, plain, subject):
        self.html = html
        self.plain = plain
        self.subject = subject

        #Composing the message
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = self.subject
        plainPart = MIMEText(self.plain, 'plain')
        htmlPart = MIMEText(self.html, 'html')
        #Order in attachement matters
        #Email client will try to render the last subpart first
        self.message.attach(plainPart)
        self.message.attach(htmlPart)


    def sendEmail(self, sender, password, receiver, server = 'smtp.gmail.com', port = 465):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context = context) as host:
            try:
                host.login(sender, password)
            except SMTPAuthenticationError:
                print("** Failed to login to server with given credentials.")
                return False
            try:
                host.sendmail(
                sender, receiver, self.message.as_string()
                )
            except:
                print("** Failed to send email to given recipients.")
                return False


if __name__ == "__main__":
    pass
    """
    ###USAGE:
    from emailer import emailer

    with open('product-announcement.html', 'r') as file:
        html = file.read()

    plain = "Hello World"
    subject = "Hi, this is the email subject"
    newMail = emailer(html = html, plain = plain, subject = subject)
    newMail.sendEmail(
    sender = "senderEmail@gmail.com",
    password = "senderPassword",
    receiver = "receiverEmail@gmail.com"
    )
    """
