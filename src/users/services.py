from django.contrib.sites.shortcuts import get_current_site
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from src.users.models import User
from src.users.utils import Util


class UserService:
    model = User

    @classmethod
    def send_mail_reset_password(cls, user, request):
        digits = str(user.created_at)
        dot = digits.index('.') + 1
        send_digits = digits[dot:dot + 6]
        email_body = (
                f"Hello {user.username}"
                + " Use this digits below to reset your password\n" +
                send_digits
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Reset your password",
        }
        Util.send_email(data)

    @classmethod
    def send_mail_register(cls, user, request):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
                "Hi "
                + user.username.title()
                + "! "
                + " Use link below to verify your email\n"
                + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data)
