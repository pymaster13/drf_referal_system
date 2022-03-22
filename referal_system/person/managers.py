from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """ Create and save any user with the given phone number
            and optional password """
        if not phone_number:
            raise ValueError('The given fields must be phone_number')

        user = self.model(phone_number=phone_number, **extra_fields)
        if user.is_superuser and password:
            # for access to admin panel
            user.set_password(password)
            user.is_active = True
        else:
            # authorization by phone number
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, phone_number, **extra_fields):
        """ Initialize of creating simple user by the given phone number """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(phone_number, password=None, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """ Initialize of creating superuser by the given phone number
            and password"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)
