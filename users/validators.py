import re
from typing import Any
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UpperCasePasswordValidator:
    """Password must contain at least 1 uppercase letter"""

    @staticmethod
    def validate(password: str, user: Any = None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _('The password must contain at least 1 uppercase letter.'),
                code='password_no_upper',
            )

    @staticmethod
    def get_help_text() -> str:
        return _(
            'Your password must contain at least 1 uppercase letter.'
        )
