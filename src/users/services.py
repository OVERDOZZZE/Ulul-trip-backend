from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from src.users.models import User
from src.users.utils import Util


class UserService:
    model = User

    @classmethod
    def send_mail_reset_password(cls, user, request):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request=request).domain
        relative_link = reverse(
            "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        absurl = "http://" + current_site + relative_link
        email_body = (
            f"Hello {user.name}"
            + " Use this link below to reset your password\n"
            + absurl
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
            + user.name.title()
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
