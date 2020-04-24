import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
            host.login(sender, password)
            host.sendmail(
            sender, receiver, self.message.as_string()
            )


if __name__ == "__main__":
    with open('product-announcement.html', 'r') as file:
        html = file.read()
    plain = "Hello World"
    subject = "Hi, this is hello world subject"
    newMail = emailer(html = html, plain = plain, subject = subject)
    newMail.sendEmail(
    sender = "zeuson164@gmail.com",
    password = "888Miles111",
    receiver = "iam.o.plus@gmail.com"
    )


    #   newMail = emailer(html, plain, subject)
