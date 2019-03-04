# -*- coding: utf-8 -*-

from django.contrib import auth


class UserCreationForm(auth.forms.UserCreationForm):
    """ Форма создания пользователя с определением модели по файлу
    конфигурации. """
    class Meta:
        model = auth.get_user_model()
        fields = ('email',)


class UserChangeForm(auth.forms.UserChangeForm):
    """ Форма редактирования пользователя с определением модели
    по файлу конфигурации. """
    class Meta:
        model = auth.get_user_model()
        fields = '__all__'
