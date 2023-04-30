import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UpperCasePasswordValidator:
    """The password must contain at least 1 uppercase letter"""

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _('The password must contain at least 1 uppercase letter.'),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            'Your password must contain at least 1 uppercase letter.'
        )
