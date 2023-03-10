import os
from datetime import datetime
import random
from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()


def path_and_rename(instance, filename):
    now = datetime.now()
    upload_to = "media"
    ext = filename.split(".")[-1]
    filename = f'{instance.tour.title}{now.strftime("%d-%m-%Y")}{random.randint}.{ext}'
    return os.path.join(upload_to, filename)
