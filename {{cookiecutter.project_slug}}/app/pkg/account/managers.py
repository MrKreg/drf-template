from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if email:
            user, created = self.get_or_create(email=email, defaults=extra_fields)
        else:
            user = self.create(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)
        return user
