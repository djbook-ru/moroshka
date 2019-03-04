# -*- coding: utf-8 -*-

from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class LocationQuerySet(models.QuerySet):
    """ Реализует часто используемые выборки для модели пользователя. """
    def all_except(self, current_user):
        """ Возвращает список геопозиций пользователей, у которых они есть. """
        qs = self.filter(lat__isnull=False, lng__isnull=False)
        return qs.exclude(pk=current_user.pk)


class CustomUserManager(auth.models.UserManager):
    """Стандартный класс для управления моделью."""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """ Создаёт и сохраняет пользователя с указанным именем,
        почтой и паролем. """
        now = timezone.now()
        if not email:
            raise ValueError(_('Email is required.'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
