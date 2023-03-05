import re
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext as _


class IsIncludeOneDigit(object):
    def validate(self, password, user=None):
        if not re.findall(r"(?:[0-9])", password):
            raise ValidationError(
                _(f"Password must include at least one digit"),
                code=f"password_no_digit",
            )

    def get_help_text(self):
        return _("Password must include at least one digit")


class IsIncludeOnlyLatyn(object):
    def validate(self, password, user=None):
        if re.findall(r"(?:[а-яА-ЯёЁ])", password):
            raise ValidationError(
                _("Password must include only latn letters"),
                code="password should contain only latn letters",
            )

    def get_help_text(self):
        return _("Password must include only latyn letters")
