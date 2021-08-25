from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from app.pkg.account.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=200, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=200, null=True, blank=True)
    email = models.EmailField(_('Email'))

    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True, blank=True)
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'), default=True, db_index=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '%s (%s)' % (self.email, self.full_name)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
