from datetime import datetime

from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],
                             body=data['email_body'], to=[data['to_email']])
        email.send()


now = datetime.now()


def path_and_rename3(instance, filename):
    upload_to = 'user_images'
    ext = filename.split('.')[-1]
    filename = f'{instance.username}{now.strftime("%d-%m-%Y %H-%M")}.{ext}'
    return os.path.join(upload_to, filename)
