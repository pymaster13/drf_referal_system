"""person application Models Configuration"""

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ Override django user model """

    phone_number = PhoneNumberField(unique=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='person_groups',
                                    verbose_name='Группы', blank=True,
                                    null=True)
    user_permissions = models.ManyToManyField(Permission,
                                              related_name='person_perms',
                                              verbose_name='Права',
                                              blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    @property
    def invited_phones(self) -> list:
        invited_objects = Invite.objects.filter(owner=self).order_by('invited')
        invited_persons = invited_objects.values('invited')
        invited_phones = [person.phone_number for person in invited_persons]
        return invited_phones

    @property
    def foreign_invite_code(self) -> str:
        try:
            invite_object = Invite.objects.get(invited=self)
            foreign_invite_code = invite_object.owner.invite_code
        except ObjectDoesNotExist:
            foreign_invite_code = ''
        return foreign_invite_code

    def __str__(self) -> str:
        return str(self.phone_number)


class Invite(models.Model):
    """ Invite model """

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='owner_invite',
                              verbose_name='Owner of invite code')
    invited = models.OneToOneField(User, 
                                   on_delete=models.CASCADE,
                                   related_name='invited_person',
                                   verbose_name='Invited person')

    def __str__(self) -> str:
        return f'Owner: {self.owner}, Invited: {self.invited}'


class Code(models.Model):
    """ SMS-code model """

    person = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='authorizing_person',
                               verbose_name='Person')
    code = models.CharField(max_length=4, verbose_name='Code')

    def __str__(self) -> str:
        return f'Person: {self.person}, code: {self.code}'
