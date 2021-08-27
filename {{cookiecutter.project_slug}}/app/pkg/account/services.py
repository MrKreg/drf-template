from django.conf import settings
from django.contrib.auth import get_user_model

from app.pkg.account.notifications.email import ActivateUserNotify, PasswordResetNotify

User = get_user_model()


class AuthService:

    @classmethod
    def _create_user(cls, **data):
        is_active = data.pop('is_active', not settings.AUTH_NEED_VERIFY_EMAIL)
        user = User.objects.create_user(**data, is_active=is_active)
        if not is_active:
            cls.send_activation_link(user)
        return user

    @classmethod
    def create_user(cls, **data):
        return cls._create_user(**data)

    @classmethod
    def update_password(cls, user, password):
        user.set_password(password)
        user.save(update_fields=['password'])

    @classmethod
    def activate(cls, user):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return user

    @classmethod
    def send_activation_link(cls, user):
        ActivateUserNotify.send_to_user(user)

    @classmethod
    def send_reset_link(cls, user):
        PasswordResetNotify.send_to_user(user)
        pass
