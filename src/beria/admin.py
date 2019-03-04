# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm
    )
from django.utils.translation import gettext_lazy as _
from sameass import logging

from src.beria import models
from src.beria import forms
from src.mixins import UserMixin

logger = logging.get_logger('admin')


class CustomUserAdmin(UserMixin, admin.ModelAdmin):
    list_display = ['email', 'last_name', 'first_name', 'sex', 'phone',
                    'want_notify_email', 'want_notify_news',
                    'is_staff', 'is_active', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (_('Personal info'), {
            'fields': ('last_name', 'first_name', 'middle_name',
                       'birth_year', 'birth_month', 'birth_day', 'sex',
                       'phone', 'address', 'title')}),
        (_('GPS'), {'fields': ('lat', 'lng')}),
        (_('Notifications'), {
            'fields': ('want_notify_email', 'want_notify_news')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')}))

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    change_password_form = AdminPasswordChangeForm


admin.site.register(models.CustomUser, CustomUserAdmin)
