from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from app.pkg.account import constants
from app.pkg.account.utils import encode_uid
from app.pkg.common.emails.service import EmailNotification
from app.pkg.common.utils.urls import build_abs_url


class ConfirmContextMixin:

    action_view_name = NotImplemented

    @classmethod
    def get_context(cls, user):
        code = constants.CONFIRM_CODE.format(
            uid=encode_uid(user.pk),
            token=default_token_generator.make_token(user)
        )
        return {
            'user': user,
            'code': code,
            'url': build_abs_url(cls.action_view_name.format(code=code))
        }


class ActivateUserNotify(ConfirmContextMixin, EmailNotification):
    template_name = 'emails/users/auth/activation_email.html'
    subject = _('Account activation on %(site_name)s')
    action_view_name = settings.WEB_ACTIVATE_URL


class PasswordResetNotify(ConfirmContextMixin, EmailNotification):
    template_name = 'emails/users/auth/password_reset_email.html'
    subject = _('Password reset on %(site_name)s')
    action_view_name = settings.WEB_RESET_URL
