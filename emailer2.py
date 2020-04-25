import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import listdir
from os.path import isfile, join
import re

class emailer:
    def __init__(self, directory, subject):

        #Listing files in the directory and finding txt, html and images
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        try:
            htmlFile = list(filter(lambda f: str(f).endswith('.html'), files))[0]
            plainFile = list(filter(lambda f: str(f).endswith('.txt'), files))[0]
            images = list(filter(lambda f: str(f).endswith(('.png', '.jpg', '.gif', '.jpeg')), files))
        except IndexError:
            print("Make sure your directory have html, txt and image files (if needed).")
            return None #No instance will be created if not txt and html file

        #Reading html and plain text file and storing them in self.html and self.plain
        with open(htmlFile, 'r') as file:
            self.html = file.read()
        with open(plainFile, 'r') as file:
            self.plain = file.read()
        self.subject = subject

        #Modifying html code image src attr to be cid:<image name w/o file extension>
        if images:
            for img in images:
                payload = "cid:" + img.split('.')[0] #discarding image file extension
                self.html = self.html.replace(img, payload)


        #Composing the message from html and plain text parts
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = self.subject
        plainPart = MIMEText(self.plain, 'plain')
        htmlPart = MIMEText(self.html, 'html')
        self.message.attach(plainPart)
        self.message.attach(htmlPart) #Email client will try to render the last subpart first


        #Attaching images to the mail with their file names to render correctly in the htmlFile
        #Not done in the loop @32 because we need to modify the html and plain first
        if images:
            for img in images:
                payload = "<{0}>".format(img.split('.')[0])
                f = open(join(directory, img), 'rb')
                msgImage = MIMEImage(f.read())
                msgImage.add_header('Content-ID', payload)
                self.message.attach(msgImage)



    def sendEmail(self, sender, password, receiver, server = 'smtp.gmail.com', port = 465):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context = context) as host:
            host.login(sender, password)
            host.sendmail(
            sender, receiver, self.message.as_string()
            )

if __name__ == "__main__":
####Modify below:
    new_email = emailer(directory = "/root/Desktop/Projects/emailer", subject = "This is test mail")
    new_email.sendEmail(
    sender = "...",
    password = "...,
    receiver = "..."
    )
