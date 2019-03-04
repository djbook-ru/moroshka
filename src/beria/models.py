# -*- coding: utf-8 -*-

"""
Класс для расширения стандартной модели пользователя Django.

Для дополнительной информации рекомендуется изучить https://habr.com/post/313764/
"""

import hashlib

from django.contrib.auth import models as auth_models
from django.core import validators
from django.core.mail import send_mail
from django.db import models as db_models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from src.beria import managers


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """ Данная модель заменяет стандартную модель пользователя.

    Все изменения и регистрация дополнительных полей должны быть описаны здесь.
    """
    SEX_MALE = 'M'
    SEX_FEMALE = 'F'
    SEX_CHOICES = (
        (SEX_MALE, _('male')),
        (SEX_FEMALE, _('female')),
    )

    ERROR_TXT_USER_EXISTS = _('A user with that email already exists.')
    email = db_models.EmailField(
        _('email address'), unique=True, max_length=255,
        help_text=_('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-_]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers and @/./+/-/_ characters.'),
                'invalid'),
            ],
        error_messages={'unique': ERROR_TXT_USER_EXISTS, })
    username = db_models.CharField(_('username'), max_length=64, null=True, blank=True)
    last_name = db_models.CharField(_('last name'), max_length=100, null=True, blank=True)
    first_name = db_models.CharField(_('first name'), max_length=100, null=True, blank=True)
    middle_name = db_models.CharField(_('middle name'), max_length=100, null=True, blank=True)
    birth_year = db_models.PositiveIntegerField(_('year of birth'), null=True, blank=True)
    birth_month = db_models.PositiveIntegerField(_('month of birth'), null=True, blank=True)
    birth_day = db_models.PositiveIntegerField(_('day of birth'), null=True, blank=True)
    sex = db_models.CharField(_('sex'), max_length=1, default=SEX_MALE, choices=SEX_CHOICES)
    phone = db_models.CharField(_('phone number'), max_length=16, null=True, blank=True)
    address = db_models.CharField(_('shipping address'), max_length=256, null=True, blank=True)
    title = db_models.CharField(_('title'), max_length=64, null=True, blank=True)

    lat = db_models.FloatField(_('latitude'), null=True, blank=True)
    lng = db_models.FloatField(_('longitude'), null=True, blank=True)

    want_notify_email = db_models.BooleanField(_('email notification'), default=False)
    want_notify_news = db_models.BooleanField(_('monthly newsletter'), default=False)

    is_staff = db_models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = db_models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = db_models.DateTimeField(_('date joined'), default=timezone.now)

    def get_full_name(self) -> str:
        """ Возвращает полное имя пользователя.
        Django требует наличие данного метода у модели. """
        name = f'{self.last_name} {self.first_name} {self.middle_name}'.strip()
        if not name:
            return self.email
        return name

    def get_short_name(self) -> str:
        """ Возвращает короткое имя. """
        return self.first_name if self.first_name else self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Отправляет электронное сообщение этому пользователю. """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def gravatar_url(self, is_secure: bool) -> str:
        """ Возвращает ссылку на граватар. """
        scheme = 'https' if is_secure else 'http'
        email_hash = hashlib.md5(self.email.strip().lower()).hexdigest()
        return f'{scheme}://www.gravatar.com/avatar/{email_hash}.jpg'

    # Поле, используемое в качестве 'username' при аутентификации
    # и в других формах
    USERNAME_FIELD = 'email'

    """
    Поле username требуется по умолчанию, добавьте здесь остальные поля, которые
    требуются для правильного регистрации пользователя.
    """
    REQUIRED_FIELDS = []

    # Связывает менеджеры с моделью
    objects = managers.CustomUserManager()
    locations = managers.LocationQuerySet.as_manager()

    class Meta:
        app_label = 'beria'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_position(self, is_secure: bool, size: int=16) -> dict:
        avatar = self.gravatar_url(is_secure)
        result = {'avatar': f'{avatar}?s={size}'}
        if self.lat and self.lng:
            result['lat'] = self.lat
            result['lng'] = self.lng
        return result
