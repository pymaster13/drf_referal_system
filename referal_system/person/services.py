"""Services to realize business logics"""

from random import choice, randint, uniform
import string
import time
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Code, Invite


User = get_user_model()


def generate_invite_code() -> str:
    """ Generate random 6-letters invite code
        for user during user creating """
    letters = string.ascii_letters + string.digits
    invite_code = ''.join(choice(letters) for _ in range(6))
    return invite_code


def generate_sms_code() -> str:
    """ Generate random 4-digits sms-code
        for user during authorization """
    code = str(randint(0, 9999))
    if len(code) < 4:
        code = (4 - len(code)) * '0' + code
    return str(code)


def get_or_create_person_by_phone(phone_number: str) -> User:
    """ Identify or create user by phone number during getting sms-code """
    person, created = User.objects.get_or_create(phone_number=phone_number)
    if created:
        person.invite_code = generate_invite_code()
        person.save()
    return person


def get_person_by_phone(phone_number: str) -> Optional[User]:
    """ Get user by phone number during authorization """
    try:
        person = User.objects.get(phone_number=phone_number)
    except ObjectDoesNotExist:
        person = None
    return person


def get_person_by_request(request) -> Optional[User]:
    """ Identify user by jwt-token in request HTTP-header """
    jwt_object = JWTAuthentication()
    try:
        header = jwt_object.get_header(request)
        raw_token = jwt_object.get_raw_token(header)
        validated_token = jwt_object.get_validated_token(raw_token)
        person = jwt_object.get_user(validated_token)
    except Exception:
        person = None
    return person


def check_user_by_invite_code(code: str) -> Optional[User]:
    """ Get user by invite code """
    try:
        person = User.objects.get(invite_code=code)
    except ObjectDoesNotExist:
        person = None
    return person


def create_sms_code(phone_number: str) -> str:
    """ Create sms-code for user during authorization """
    person = get_or_create_person_by_phone(phone_number)
    code = generate_sms_code()
    if Code.objects.filter(person=person).exists():
        Code.objects.filter(person=person).delete()
    Code.objects.create(person=person, code=code)

    delay = uniform(1.0, 2.0)
    time.sleep(delay)

    return code


def generate_tokens(person: User) -> dict:
    """ Generate tokens for authorization of user """
    refresh = RefreshToken.for_user(person)
    tokens = {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
    return tokens


def authorize(phone_number: str, code: str) -> Optional[dict]:
    """ Return tokens for authorizing user """
    person = get_person_by_phone(phone_number)
    if not person:
        return {'error': 'user does not exist'}
    try:
        code = Code.objects.get(person=person, code=code)
        code.delete()
    except ObjectDoesNotExist:
        return {'error': 'checking code failed'}

    tokens = generate_tokens(person)

    person.is_active = True
    person.save()

    return tokens


def form_profile_data(request) -> dict:
    """ Return information about current user """
    person = get_person_by_request(request)

    result = {}
    result['phone_number'] = person.__str__()
    result['invite_code'] = person.invite_code
    result['invited_users'] = person.invited_phones
    result['activated_foreign_invite_code'] = person.foreign_invite_code
    return result


def implement_invite(request, invite_code: str) -> dict:
    """ Implement foreign invite code for current user """
    self_person = get_person_by_request(request)
    owner_invite_person = check_user_by_invite_code(invite_code)
    if not owner_invite_person:
        return {'error': 'invite code does not exist'}
    if not owner_invite_person.is_active:
        return {'error': "you can't activate inactive user's invite code"}
    if self_person.foreign_invite_code:
        return {'error': 'code exists but you activated invite already'}

    Invite.objects.create(owner=owner_invite_person, invited=self_person)

    return {'result': f'invite code {owner_invite_person} is accepted'}
